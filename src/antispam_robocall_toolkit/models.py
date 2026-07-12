"""Data models for API responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ValidationResponse(BaseModel):
    ani: str
    normalized_ani: str
    dnis: str | None = None
    source: str | None = None
    risk_score: int = Field(ge=0, le=100)
    decision: str
    reason: str
    source_hits: list[str]
    matched_records: int
    recommended_action: str


class HealthResponse(BaseModel):
    status: str
    database: str
