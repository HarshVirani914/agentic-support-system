# AI Customer Support - Frontend

Modern, responsive chat interface for the Agentic AI Customer Support System built with Next.js, TypeScript, and shadcn/ui.

## Features

- **Real-time Chat Interface** - Clean, intuitive messaging UI with user and assistant roles
- **Category-Based Routing** - Visual indicators showing which AI agent handled the query (Order, Shipping, General)
- **Source Citations** - Collapsible source panel with relevance scores for transparency
- **Smart Error Handling** - User-friendly error messages with automatic retry
- **Loading States** - Elegant loading indicators during AI processing
- **Copy to Clipboard** - One-click copy for AI responses
- **Clear Chat** - Reset conversation with a single click
- **Sample Questions** - Quick-start prompts for new users
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Professional Typography** - Inter font for optimal readability

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **State Management**: React Hooks (useState, useEffect)

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with Inter font
│   ├── page.tsx            # Main chat page
│   └── globals.css         # Global styles and theme
├── components/
│   ├── chat/
│   │   ├── chat-interface.tsx   # Main chat container
│   │   └── chat-message.tsx     # Individual message component
│   └── ui/                      # shadcn components
├── lib/
│   ├── api.ts              # Backend API client
│   ├── types.ts            # TypeScript interfaces
│   └── utils.ts            # Helper functions
└── .env.local              # Environment variables
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies:**

```bash
npm install
```

2. **Configure environment variables:**

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run development server:**

```bash
npm run dev
```

4. **Open in browser:**

```
http://localhost:3000
```

## Environment Variables

| Variable              | Description          | Default                 |
| --------------------- | -------------------- | ----------------------- |
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

## Component Architecture

### ChatInterface

Main container managing:

- Message history state
- User input handling
- API communication
- Error and loading states
- Auto-scroll behavior

### ChatMessage

Displays individual messages with:

- Role-based styling (user vs assistant)
- Category badges (color-coded by query type)
- Collapsible source citations
- Copy-to-clipboard functionality
- Relevance score indicators

## Key Features

### Category Badges

Each AI response shows which specialized agent handled the query:

- **Blue** - Order-related queries (refunds, purchases, billing)
- **Green** - Shipping-related queries (delivery, tracking)
- **Gray** - General queries (accounts, policies, info)

### Source Citations

Transparent RAG (Retrieval-Augmented Generation) system:

- Shows sources used to generate the answer
- Displays relevance scores (0-100%)
- Collapsible to reduce UI clutter
- Helps users verify information accuracy

### Error Handling

Graceful error management:

- Invalid input validation (empty messages)
- Network error handling
- Backend error messages displayed clearly
- No app crashes from errors

## API Integration

The frontend communicates with the FastAPI backend via REST API:

**Endpoint:** `POST /api/chat`

**Request:**

```typescript
{
  message: string;
  limit?: number;  // Number of sources (default: 3)
}
```

**Response:**

```typescript
{
  answer: string;
  sources: Array<{
    text: string;
    score: number;
  }>;
  category: string; // "order" | "shipping" | "general"
}
```

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Start production server
npm start
```

## Deployment

### Deploy to Vercel (Recommended)

1. **Push to GitHub:**

```bash
git push origin main
```

2. **Import to Vercel:**

- Go to [vercel.com](https://vercel.com)
- Import your GitHub repository
- Set environment variables
- Deploy

3. **Update backend URL:**

```bash
# Production environment variable
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Deploy to Netlify

1. **Build command:** `npm run build`
2. **Publish directory:** `.next`
3. **Environment variables:** Set `NEXT_PUBLIC_API_URL`

## Accessibility

- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard navigation support
- Color contrast WCAG AA compliant
- Focus management for dynamic content
- Loading state announcements

## Troubleshooting

### Backend Connection Issues

**Problem:** Cannot connect to backend
**Solution:**

- Verify backend is running on port 8000
- Check CORS settings in backend
- Confirm `NEXT_PUBLIC_API_URL` is set correctly

### Build Errors

**Problem:** TypeScript errors during build
**Solution:**

```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

### Styling Issues

**Problem:** Tailwind classes not working
**Solution:**

```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

## Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit: `git commit -m "Add new feature"`
3. Push to branch: `git push origin feature/new-feature`
4. Open pull request

## License

This project is part of a portfolio demonstration.

## Acknowledgments

- Built with [Next.js](https://nextjs.org)
- UI components from [shadcn/ui](https://ui.shadcn.com)
- Icons from [Lucide](https://lucide.dev)
