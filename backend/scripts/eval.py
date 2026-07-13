"""
Evaluation Suite

Runs every case in `scripts/eval_dataset.py` through the live agent graph
(`run_agent`, including hybrid search, reranking, and the reflection/grading
loop), then scores the resulting (question, answer, retrieved contexts,
ground truth) tuples with RAGAS metrics using a Groq model as the judge LLM.
Writes a markdown scorecard to `backend/eval_results.md`.

Usage:
    python scripts/eval.py

Note on the RAGAS API used here: the installed version (ragas==0.3.9) uses
the "single turn sample" schema introduced in RAGAS 0.2+, where dataset
fields are named `user_input` / `response` / `retrieved_contexts` /
`reference` (not the older `question` / `answer` / `contexts` /
`ground_truth` names from the original task sketch). This script builds an
`EvaluationDataset` of `SingleTurnSample` objects accordingly.

Two adaptations were needed to run reliably against Groq's free tier:
- `AnswerRelevancy`'s default `strictness=3` asks the judge LLM for 3
  completions in a single request (`n=3`), which Groq's API rejects
  ("'n': number must be at most 1"). We use `strictness=1` instead.
- The judge model is `llama-3.1-8b-instant` rather than the heavier
  `llama-3.3-70b-versatile` used elsewhere in the app, to stay within the
  free tier's per-model daily token budget across ~24 cases x 3 metrics of
  judge calls (a first run against llama-3.3-70b-versatile exhausted the
  70B model's 100k TPD budget partway through and left many cases as NaN).

Agent run results are cached to `scripts/.eval_cache.json` (keyed by
question) so that re-running the RAGAS scoring step after a rate-limit
interruption doesn't re-burn quota re-running the agent itself.
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import faithfulness, AnswerRelevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_groq import ChatGroq

from app.agents.graph import run_agent
from app.config import settings
from app.core.embeddings import embedding_model
from scripts.eval_dataset import EVAL_CASES

CACHE_PATH = Path(__file__).parent / ".eval_cache.json"
JUDGE_MODEL = "llama-3.1-8b-instant"


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text())
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_PATH.write_text(json.dumps(cache, indent=2))


def run_eval(use_cache: bool = True):
    samples = []
    per_case_rows = []
    cache = _load_cache() if use_cache else {}

    for idx, case in enumerate(EVAL_CASES):
        question = case["question"]
        if use_cache and question in cache:
            print(f"[{idx + 1}/{len(EVAL_CASES)}] Using cached agent result for: {question!r}")
            result = cache[question]
        else:
            print(f"[{idx + 1}/{len(EVAL_CASES)}] Running agent on: {question!r}")
            raw_result = run_agent(question, thread_id=f"eval-{idx}")
            result = {
                "answer": raw_result["answer"],
                "sources": raw_result["sources"],
                "retry_count": raw_result.get("retry_count", 0),
                "grounded": raw_result.get("grounded", True),
            }
            cache[question] = result
            _save_cache(cache)

        contexts = [s["text"] for s in result["sources"]] or [""]

        samples.append(
            SingleTurnSample(
                user_input=question,
                response=result["answer"],
                retrieved_contexts=contexts,
                reference=case["ground_truth"],
            )
        )
        per_case_rows.append(
            {
                "category": case["category"],
                "question": question,
                "retry_count": result.get("retry_count", 0),
                "grounded": result.get("grounded", True),
            }
        )

    dataset = EvaluationDataset(samples=samples)

    judge_llm = LangchainLLMWrapper(
        ChatGroq(model=JUDGE_MODEL, groq_api_key=settings.GROQ_API_KEY)
    )
    # answer_relevancy needs an embedding model to compare generated questions
    # against the original question; RAGAS defaults to OpenAI, which we don't
    # have credentials for, so reuse the project's Gemini embedding model.
    judge_embeddings = LangchainEmbeddingsWrapper(embedding_model.model)
    # strictness=1 avoids requesting multiple (n>1) completions per call,
    # which Groq's API rejects.
    answer_relevancy = AnswerRelevancy(strictness=1)

    print(f"\nScoring with RAGAS (faithfulness, answer_relevancy, context_precision) "
          f"using judge model {JUDGE_MODEL}...")
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
        llm=judge_llm,
        embeddings=judge_embeddings,
    )

    df = result.to_pandas()
    metric_cols = ["faithfulness", "answer_relevancy", "context_precision"]
    overall_scores = df[metric_cols].mean()

    # Per-category breakdown
    df["category"] = [row["category"] for row in per_case_rows]
    category_scores = df.groupby("category")[metric_cols].mean()

    retried_count = sum(1 for row in per_case_rows if row["retry_count"] > 0)

    report_lines = ["# Evaluation Results\n"]
    report_lines.append(f"Ran {len(EVAL_CASES)} test cases against the live agent graph "
                         f"(hybrid search + reranking + reflection loop), scored with "
                         f"RAGAS using Groq `{JUDGE_MODEL}` as the judge LLM.\n")
    report_lines.append(f"Cases that triggered at least one reflection retry: {retried_count}/{len(EVAL_CASES)}\n")

    report_lines.append("## Overall Scores\n")
    report_lines.append("| Metric | Score |\n|---|---|")
    for metric, score in overall_scores.items():
        report_lines.append(f"| {metric} | {score:.3f} |")

    report_lines.append("\n## Scores by Category\n")
    report_lines.append("| Category | Faithfulness | Answer Relevancy | Context Precision |\n"
                         "|---|---|---|---|")
    for category, row in category_scores.iterrows():
        report_lines.append(
            f"| {category} | {row['faithfulness']:.3f} | {row['answer_relevancy']:.3f} | "
            f"{row['context_precision']:.3f} |"
        )

    report_lines.append("\n## Per-Case Detail\n")
    report_lines.append("| # | Category | Question | Faithfulness | Answer Relevancy | Context Precision | Retries |\n"
                         "|---|---|---|---|---|---|---|")
    for i, row in df.iterrows():
        case = per_case_rows[i]
        report_lines.append(
            f"| {i + 1} | {case['category']} | {case['question']} | "
            f"{row['faithfulness']:.3f} | {row['answer_relevancy']:.3f} | "
            f"{row['context_precision']:.3f} | {case['retry_count']} |"
        )

    report = "\n".join(report_lines) + "\n"

    output_path = Path(__file__).parent.parent / "eval_results.md"
    output_path.write_text(report)
    print(report)
    print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    run_eval()
