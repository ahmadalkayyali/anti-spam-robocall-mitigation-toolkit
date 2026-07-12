from antispam_robocall_toolkit.normalize import normalize_ani, cube_regex_for_ani


def test_normalize_nanp_10_digit():
    assert normalize_ani("5551234567") == "+15551234567"


def test_normalize_nanp_11_digit():
    assert normalize_ani("1-555-123-4567") == "+15551234567"


def test_normalize_sip_uri():
    assert normalize_ani("sip:+15551234567@example.com") == "+15551234567"


def test_cube_regex():
    assert cube_regex_for_ani("+15551234567") == "/^\\+15551234567$/"
