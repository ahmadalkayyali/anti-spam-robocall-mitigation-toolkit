"""Optional Twilio Lookup adapter placeholder.

This project does not require Twilio. Keep credentials out of GitHub and use
Twilio only when your organization has approved API usage and cost.
"""

from __future__ import annotations


def map_twilio_lookup_to_risk(line_type: str | None, carrier_name: str | None = None) -> dict:
    """Convert a Twilio Lookup result into a generic risk record suggestion.

    This function intentionally does not call Twilio. It maps an already-obtained
    enrichment result into the toolkit's risk model.
    """
    normalized_type = (line_type or "").strip().lower()
    if normalized_type in {"non-fixed voip", "non_fixed_voip"}:
        score = 55
        level = "medium"
        reason = "Twilio Lookup indicated non-fixed VoIP line type"
    elif normalized_type in {"toll-free", "toll_free"}:
        score = 35
        level = "low"
        reason = "Twilio Lookup indicated toll-free line type"
    else:
        score = 10
        level = "info"
        reason = "Twilio Lookup enrichment only"

    return {
        "source_name": "TwilioLookup",
        "source_type": "enrichment",
        "risk_level": level,
        "risk_score": score,
        "reason": reason,
        "notes": f"Carrier={carrier_name or 'unknown'}; LineType={line_type or 'unknown'}",
    }
