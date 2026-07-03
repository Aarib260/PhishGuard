#  PhishGuard

**AI-powered phishing detection for URLs, emails, and messages.**

PhishGuard analyzes a pasted URL, email, or message and returns a 0–100 risk score, a Safe/Suspicious/Dangerous label, and a plain-language explanation of why it was flagged — combining deterministic security heuristics with an LLM-generated explanation layer.

---

## How it works

Rather than asking an LLM to "decide" if something is phishing, PhishGuard runs a rule-based detection engine first, then uses an LLM only to explain the findings in plain language. This keeps the verdict deterministic and auditable, while still giving users a clear, human-readable explanation.


Input (URL / email / message)
        │
        ▼

   Heuristic Engine      
  • URL structure         
  • TLD reputation        
  • Typosquatting/brand    
  • IP-based URL detection 
  • Urgency/manipulation   
  • Credential requests    
  • Attachment language    
        │
        ▼
   Risk Score (0–100)
        │
        ▼

   LLM (via OpenRouter)  
  Explains the signals    
  in plain language and    
  gives safety advice      
        │
        ▼
  Result + saved to history


## Features
```
 **URL analysis** — HTTPS check, suspicious TLDs, typosquatting/brand impersonation, IP-based URLs
 **Email/message analysis** — urgency & manipulation language, credential-harvesting requests, suspicious attachment phrasing
 **AI explanation** — plain-language reasoning and 3 concrete safety recommendations per scan
 **Scan history** — every scan is saved and viewable on a dedicated history page
 **Graceful degradation** — if the AI explanation call fails or times out, the heuristic score/label still return successfully
``
## Tech stack

 Layer | Technology 

 Frontend | Next.js (App Router) + Tailwind CSS 
 Backend | FastAPI 
 Database | PostgreSQL (hosted on Neon) 
 AI | LLM via OpenRouter (OpenAI-compatible SDK)
 Deployment | Vercel (frontend) + Railway (backend) 

## Project structure


phishguard/
├── backend/
│   ├── main.py
│   ├── routers/scan.py
│   ├── services/
│   │   ├── heuristics/
│   │   │   ├── url_analysis.py
│   │   │   ├── keyword_scanner.py
│   │   │   └── scoring.py
│   │   └── llm_service.py
│   └── models/history.py
└── frontend/
    └── app/
        ├── page.tsx
        └── history/page.tsx


## Running locally

**Backend**
```
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# create a .env with DATABASE_URL and OPENAI_API_KEY
uvicorn main:app --reload
``

**Frontend**
```
cd frontend
npm install
# create a .env.local with NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
npm run dev
``
## License

MIT
