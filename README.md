# PhishGuard

PhishGuard is a phishing detection tool that analyzes URLs, emails, and text messages. It gives each scan a risk score (0–100), classifies it as Safe, Suspicious, or Dangerous, and explains why the content was flagged.

Instead of relying entirely on AI to make a decision, the application uses a rule-based detection engine for the verdict and an LLM only to generate an easy-to-understand explanation.

---

## How it works

When a user submits a URL, email, or message:

1. The input is analyzed using a set of phishing detection rules.
2. The rules generate a risk score based on suspicious indicators.
3. The score is converted into a security label.
4. The findings are sent to an LLM through OpenRouter, which explains the detected issues in plain English and suggests what the user should do next.
5. The completed scan is stored in the history database.

The heuristic engine looks for things like:

- Suspicious URL structure
- Risky or uncommon top-level domains
- Typosquatting and brand impersonation
- URLs that use IP addresses instead of domain names
- Urgent or manipulative language
- Requests for passwords or personal information
- Suspicious attachment-related wording

If the AI explanation cannot be generated (for example because of an API timeout), the scan still completes normally using the heuristic results.

---

## Features

- Analyze URLs for common phishing indicators
- Scan emails and messages for phishing language
- Generate AI-powered explanations of detected threats
- Show practical safety recommendations after each scan
- Save previous scans to a history page
- Continue working even if the AI service is unavailable

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js (App Router), Tailwind CSS |
| Backend | FastAPI |
| Database | PostgreSQL (Neon) |
| AI | OpenRouter (OpenAI-compatible API) |
| Deployment | Vercel (Frontend), Railway (Backend) |

---

## Project Structure

```
phishguard/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   └── scan.py
│   ├── services/
│   │   ├── heuristics/
│   │   │   ├── url_analysis.py
│   │   │   ├── keyword_scanner.py
│   │   │   └── scoring.py
│   │   └── llm_service.py
│   └── models/
│       └── history.py
└── frontend/
    └── app/
        ├── page.tsx
        └── history/
            └── page.tsx
```

---

## Running Locally

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openrouter_api_key
```

Start the backend:

```bash
uvicorn main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install
```

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Start the development server:

```bash
npm run dev
```

---

## License

This project is licensed under the MIT License.
