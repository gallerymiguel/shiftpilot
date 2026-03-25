# ShiftPilot – AI Scheduling Assistant (MVP)

ShiftPilot is an AI-powered scheduling assistant that automates employee call-out handling and generates intelligent coverage recommendations using real company policies.

This project demonstrates modern AI architecture patterns including orchestration workflows, RAG (Retrieval-Augmented Generation), and multi-service integration.

---

## 🚀 What It Does

When an employee sends a message like:

> "I can't make it tonight"

The system:

1. Receives the message via Telegram
2. Triggers an n8n workflow
3. Sends the message to a FastAPI backend
4. Interprets the request using OpenAI
5. Retrieves relevant staffing policies from a vector database (Chroma)
6. Generates a structured recommendation
7. Sends a response back via Telegram with:
   - Recommended employees to cover the shift
   - Reasoning based on policy
   - A ready-to-send outreach message

---

## 🧠 Architecture Overview

```

Telegram → n8n → FastAPI → (OpenAI + Chroma + Postgres) → n8n → Telegram

````

---

## Key Features

- AI-powered call-out interpretation
- Policy-aware decision making (RAG)
- Automated coverage recommendations
- Real-time messaging integration (Telegram)
- Workflow orchestration with n8n
- Structured AI outputs (JSON-based responses)

---

## 🛠 Tech Stack

### Frontend / Interface
- Telegram Bot API

### Orchestration
- n8n

### Backend
- FastAPI (Python)

### AI & Data
- OpenAI API (interpretation + reasoning)
- Chroma (vector database for policy retrieval)
- PostgreSQL (structured data storage)

### Infrastructure
- Docker + Docker Compose

---

## 📦 Example Output

```json
{
  "status": "call_out_recorded",
  "employee": "Maria",
  "shift_id": 3,
  "interpretation": {
    "intent": "call_out",
    "urgency": "high"
  },
  "recommendations": [
    {
      "name": "Josh",
      "role": "dedicated",
      "reason": "same store priority"
    }
  ],
  "explanation": "Dedicated employees from the same store are prioritized...",
  "draft_message": "Hi Josh, we need coverage for tonight..."
}
````

---

## Why This Project Matters

This project demonstrates real-world AI system design beyond simple prompts:

* Orchestrated workflows instead of single API calls
* Retrieval-Augmented Generation (RAG)
* Multi-system integration
* Production-style architecture

---

## Future Improvements

* Persistent employee behavior tracking (true memory)
* SMS integration (Twilio)
* Scheduling optimization logic
* Admin dashboard
* Multi-store scaling

---
