"""Phone number normalization utilities.

This intentionally avoids any private/internal numbering assumptions. The default
behavior targets NANP-style numbers but accepts already-normalized E.164 values.
"""

from __future__ import annotations

import re

_DIGIT_RE = re.compile(r"\D+")


def normalize_ani(value: str | int | None, default_country_code: str = "1") -> str:
    """Normalize a caller ANI to a basic E.164-like value.

    Args:
        value: Raw caller number such as ``5551234567``, ``+15551234567``,
            ``1-555-123-4567``, or ``sip:+15551234567@example.com``.
        default_country_code: Country code to add when the input has 10 digits.

    Returns:
        A normalized value like ``+15551234567``. If the input is empty, returns
        an empty string.
    """
    if value is None:
        return ""

    raw = str(value).strip()
    if not raw:
        return ""

    # Pull number from common SIP URI patterns.
    if raw.lower().startswith("sip:"):
        raw = raw[4:].split("@", 1)[0]

    has_plus = raw.startswith("+")
    digits = _DIGIT_RE.sub("", raw)

    if not digits:
        return ""

    # NANP 10-digit local number.
    if len(digits) == 10:
        return f"+{default_country_code}{digits}"

    # NANP 11-digit number beginning with 1.
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"

    # Keep other international-looking numbers as +digits.
    if has_plus or len(digits) > 10:
        return f"+{digits}"

    return digits


def cube_regex_for_ani(normalized_ani: str) -> str:
    """Return a Cisco voice translation-rule regex for an exact ANI match."""
    escaped = normalized_ani.replace("+", "\\+")
    return f"/^{escaped}$/"
