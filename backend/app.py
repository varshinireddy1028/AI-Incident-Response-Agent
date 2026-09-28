from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hindsight_client import Hindsight
import requests

app = FastAPI(title="AI Incident Response Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Hindsight
memory = Hindsight(base_url="http://localhost:8888")

BANK_ID = "incident-response"

# Ollama
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:1b"


class Incident(BaseModel):
    description: str


@app.get("/")
def home():
    return {
        "message": "AI Incident Response Agent is running!"
    }


@app.post("/analyze")
def analyze_incident(incident: Incident):

    # Step 1: Recall similar incidents from Hindsight
    results = memory.recall(
        bank_id=BANK_ID,
        query=incident.description
    )

    memories = []

    for result in results.results:
        memories.append(result.text)

    # Step 2: Give the recalled memories to the AI
    memory_text = "\n".join(
        f"- {item}" for item in memories
    )

    prompt = f"""
You are an AI Incident Response Agent.

A new production incident has occurred:

{incident.description}

Here are similar incidents remembered from previous incidents:

{memory_text}

Analyze the current incident using the previous incidents as context.

Give a concise response with:

1. Possible root cause
2. What to check first
3. Recommended troubleshooting steps
4. How the previous incident may help

Do not invent information that is not supported by the incident or memories.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    ai_response = response.json()["message"]["content"]

    return {
        "incident": incident.description,
        "similar_incidents": memories,
        "ai_analysis": ai_response
    }


@app.post("/resolve")
async def resolve_incident(data: dict):

    incident = data.get("incident", "")
    root_cause = data.get("root_cause", "")
    resolution = data.get("resolution", "")
    outcome = data.get("outcome", "")

    resolve_memory = Hindsight(base_url="http://localhost:8888")

    await resolve_memory.aretain(
        bank_id=BANK_ID,
        content=f"""
Incident: {incident}
Root cause: {root_cause}
Resolution: {resolution}
Outcome: {outcome}
""",
        context="production incident"
    )

    return {
        "message": "Incident resolution stored in Hindsight successfully!"
    }