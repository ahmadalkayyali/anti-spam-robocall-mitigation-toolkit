"""FastAPI service for ANI validation."""

from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException, Query
from dotenv import load_dotenv

from .database import init_db
from .models import HealthResponse, ValidationResponse
from .scoring import validate_ani

load_dotenv()

DB_PATH = os.getenv("SPAMGUARD_DB", "data/output/ani_risk.sqlite")
API_KEY = os.getenv("SPAMGUARD_API_KEY", "")

app = FastAPI(
    title="Anti-Spam and Robocall Mitigation API",
    description="Source-agnostic ANI risk validation API for Cisco voice/contact center environments.",
    version="1.0.0",
)


def _check_api_key(x_api_key: str | None) -> None:
    # API key is optional for local demos. Set SPAMGUARD_API_KEY to enforce it.
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    init_db(DB_PATH)
    return HealthResponse(status="ok", database=DB_PATH)


@app.get("/api/v1/validate", response_model=ValidationResponse)
def validate(
    ani: str = Query(..., description="Calling ANI to validate"),
    dnis: str | None = Query(None, description="Optional called number/DNIS"),
    source: str | None = Query(None, description="Optional caller/source such as cvp, icm, cube-report"),
    x_api_key: str | None = Header(default=None),
) -> ValidationResponse:
    _check_api_key(x_api_key)
    return validate_ani(ani=ani, dnis=dnis, source=source, db_path=DB_PATH)
