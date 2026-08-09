# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Multi-Model SaaS Product — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Multi-Model SaaS Product"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


FLEETS = {"fast": "mock-small", "default": "mock-mid", "frontier": "mock-frontier"}

class GenIn(BaseModel):
    prompt: str
    tier: str = "auto"

def pick(tier: str, prompt: str) -> str:
    if tier in FLEETS:
        return FLEETS[tier]
    return FLEETS["frontier"] if len(prompt) > 80 else FLEETS["fast"]

@app.post("/generate")
async def generate(body: GenIn):
    model = pick(body.tier, body.prompt)
    local = MockLLM(model=model)
    text = await local.complete(body.prompt)
    return {"chosen_model": model, "text": text}
