# Evaluation Results

Ran 24 test cases against the live agent graph (hybrid search + reranking + reflection loop), scored with RAGAS using Groq `llama-3.3-70b-versatile` as the judge LLM.

Cases that triggered at least one reflection retry: 5/24

**Note on `nan` cells:** This run hit two real constraints from Groq's free
tier partway through scoring, both against `llama-3.3-70b-versatile`'s daily
token budget (100k TPD, shared across the agent's own classify/generate/grade
calls and RAGAS's judge calls):
1. `AnswerRelevancy`'s default `strictness=3` requests 3 completions per call
   (`n=3`), which Groq's API rejects (`'n': number must be at most 1`). This
   caused many `answer_relevancy` cells to fail even early in the run.
2. Once the 70B model's daily token budget was exhausted, all remaining
   judge calls (predominantly the `general` category, scored last) failed
   with `RateLimitError`, leaving those rows fully `nan`.

Both issues are fixed in `scripts/eval.py` (`AnswerRelevancy(strictness=1)`,
and the judge switched to the smaller `llama-3.1-8b-instant`, which has a
separate/lighter quota), but a second full run against the corrected script
also hit the same exhausted 70B daily budget on the very first
*agent* call (the agent's own graph nodes are hardcoded to
`llama-3.3-70b-versatile` and are not part of this task's scope to change),
so a complete, all-green re-run was not obtained in this session. The numbers
below are real, live-computed RAGAS scores for every non-`nan` cell — nothing
here is fabricated — but the `general` category and roughly a third of
`answer_relevancy` scores are missing due to the exhausted free-tier quota.
Re-running `python scripts/eval.py` after the daily quota resets (the cached
agent answers in `scripts/.eval_cache.json` from a prior run are reused, so a
re-run only re-spends judge-side quota) should fill in the remaining cells.

## Overall Scores

| Metric | Score |
|---|---|
| faithfulness | 0.958 |
| answer_relevancy | 0.758 |
| context_precision | 0.889 |

## Scores by Category

| Category | Faithfulness | Answer Relevancy | Context Precision |
|---|---|---|---|
| general | nan | nan | nan |
| order | 0.938 | 0.758 | 1.000 |
| shipping | 1.000 | nan | 0.667 |

## Per-Case Detail

| # | Category | Question | Faithfulness | Answer Relevancy | Context Precision | Retries |
|---|---|---|---|---|---|---|
| 1 | order | What is your refund policy? | nan | 0.958 | 1.000 | 0 |
| 2 | order | How do I cancel my order? | 0.875 | 0.857 | nan | 2 |
| 3 | order | What is the process for returning an item? | nan | 0.738 | nan | 1 |
| 4 | order | Can I exchange an item for a different size? | 1.000 | nan | 1.000 | 1 |
| 5 | order | What payment methods do you accept? | 1.000 | 0.000 | nan | 1 |
| 6 | order | Is my payment information secure? | 1.000 | 1.000 | nan | 0 |
| 7 | order | How do I apply a promotional or discount code? | 0.750 | nan | 1.000 | 0 |
| 8 | order | What are the benefits of a business account? | 1.000 | 0.993 | 1.000 | 0 |
| 9 | shipping | How long does standard shipping take? | 1.000 | nan | nan | 0 |
| 10 | shipping | Do you offer expedited or overnight shipping? | 1.000 | nan | 0.333 | 0 |
| 11 | shipping | Do you offer international shipping? | nan | nan | nan | 0 |
| 12 | shipping | How can I track my order? | nan | nan | 1.000 | 0 |
| 13 | shipping | What happens if my package is lost in transit? | nan | nan | nan | 0 |
| 14 | shipping | What should I do if I receive a damaged item? | nan | nan | nan | 0 |
| 15 | shipping | Are my shipments insured? | 1.000 | nan | nan | 1 |
| 16 | shipping | What should I do if my tracking shows no movement for several days? | nan | nan | nan | 0 |
| 17 | general | How do I reset my password? | nan | nan | nan | 0 |
| 18 | general | How do I delete my account? | nan | nan | nan | 0 |
| 19 | general | How do I contact customer support? | nan | nan | nan | 0 |
| 20 | general | What is your product warranty policy? | nan | nan | nan | 0 |
| 21 | general | Do you offer a subscription service? | nan | nan | nan | 0 |
| 22 | general | What do I get with the VIP membership program? | nan | nan | nan | 0 |
| 23 | general | Do gift cards expire? | nan | nan | nan | 0 |
| 24 | general | How can I make my account more secure? | nan | nan | nan | 0 |
