# Anti-Spam and Robocall Mitigation Toolkit

Source-agnostic ANI risk validation for Cisco voice and contact center environments.

This toolkit helps voice engineers validate inbound ANI values against trusted spam, robocall, carrier, DNO, internal complaint, and custom risk datasets before deciding how a call should be handled. It is designed for Cisco CUBE, CVP, ICM, UCCE, CUCM, SIP trunk, and enterprise contact center workflows.

> This repository uses dummy sample data only. Do not commit production call records, customer data, private ANI evidence, API keys, carrier files, internal IPs, usernames, passwords, or organization-specific blocklists.

## Why this project exists

Robocalls, spoofed caller ID, fraud attempts, and abusive calling campaigns create operational risk for enterprise contact centers. This project provides a reusable technical framework to turn trusted ANI intelligence into routing, reporting, and mitigation decisions.

The project is **not tied to one database**. You can bring your own source:

- Internal enterprise spam/robocall ANI lists
- Carrier DNO or abuse feeds
- Fraud investigation records
- Customer complaint data
- Twilio Lookup enrichment exports
- FCC/provider reference exports
- Lumen/carrier blocklists where authorized
- Any custom CSV or API-based ANI risk source

## Main use cases

- Validate ANI before routing a call to a Cisco contact center queue
- Tag risky calls for reporting and investigation
- Send suspicious calls to IVR verification before queueing
- Route high-risk calls to a lower-priority or review queue
- Generate reviewed Cisco CUBE call-block rules for confirmed high-risk ANI values
- Build reporting around repeated robocall patterns, spoofing attempts, and abusive traffic

## Architecture

```text
Inbound SIP Call
   |
   v
Cisco CUBE
   |
   v
CUCM / CVP / ICM / UCCE
   |
   v
ANI Risk Validation API
   |
   v
Local ANI Risk Database
   |
   v
Decision: ALLOW / WATCH / CHALLENGE / SPAM_QUEUE / BLOCK / REVIEW
```

## Quick start

### 1. Clone your GitHub repo

```bash
git clone https://github.com/YOUR_USERNAME/anti-spam-robocall-mitigation-toolkit.git
cd anti-spam-robocall-mitigation-toolkit
```

### 2. Create a Python virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Build a local SQLite database from sample data

```bash
python scripts/build_db.py --source data/samples/ani_risk_sources_sample.csv --db data/output/ani_risk.sqlite
```

### 5. Query a test ANI locally

```bash
python scripts/query_ani.py --ani +15551234567 --db data/output/ani_risk.sqlite
```

Expected result:

```json
{
  "ani": "+15551234567",
  "normalized_ani": "+15551234567",
  "risk_score": 95,
  "decision": "BLOCK",
  "source_hits": ["InternalSpamList"],
  "reason": "Repeated robocall pattern in enterprise contact center"
}
```

### 6. Run the REST API

```bash
uvicorn antispam_robocall_toolkit.api:app --app-dir src --reload --host 0.0.0.0 --port 8080
```

Test it:

```bash
curl "http://localhost:8080/api/v1/validate?ani=+15551234567&dnis=18005550100&source=cvp"
```

## CSV input format

Use `data/samples/ani_risk_sources_sample.csv` as the template.

Required columns:

```csv
ani,source_name
```

Recommended columns:

```csv
ani,source_name,source_type,risk_level,risk_score,reason,first_seen,last_seen,active,notes
```

Example:

```csv
ani,source_name,source_type,risk_level,risk_score,reason,first_seen,last_seen,active,notes
+15551234567,InternalSpamList,internal,high,95,Repeated robocall pattern,2026-01-01,2026-07-01,1,Dummy sample only
+15557654321,CarrierDNO,dno,high,90,Do-not-originate match,2026-02-01,2026-07-02,1,Dummy sample only
+15559876543,TwilioLookup,enrichment,medium,55,Non-fixed VoIP source,2026-03-01,2026-07-03,1,Dummy sample only
```

## REST API response

```json
{
  "ani": "+15551234567",
  "normalized_ani": "+15551234567",
  "dnis": "18005550100",
  "risk_score": 95,
  "decision": "BLOCK",
  "reason": "Repeated robocall pattern in enterprise contact center",
  "source_hits": ["InternalSpamList"],
  "matched_records": 1,
  "recommended_action": "Reject, disconnect, or route to controlled spam treatment after operational review"
}
```

## Decision model

| Score | Decision | Suggested action |
|---:|---|---|
| 0-24 | `ALLOW` | Route normally |
| 25-49 | `WATCH` | Route normally and tag for reporting |
| 50-74 | `CHALLENGE` | Send to IVR verification or enhanced treatment |
| 75-89 | `SPAM_QUEUE` | Route to lower-priority/special handling queue |
| 90-100 | `BLOCK` | Block only after operational/legal review |

The scoring rules are intentionally transparent and easy to change in `src/antispam_robocall_toolkit/scoring.py`.

## Cisco CUBE option

For confirmed high-risk numbers, generate a CUBE translation-rule block profile:

```bash
python scripts/generate_cube_blocklist.py \
  --input data/samples/ani_risk_sources_sample.csv \
  --output data/output/cube_spam_blocklist.cfg \
  --rule-id 901 \
  --profile-name SPAM_CALL_BLOCK \
  --min-score 90
```

Example generated config:

```cisco
voice translation-rule 901
 rule 1 reject /^\+15551234567$/
!
voice translation-profile SPAM_CALL_BLOCK
 translate calling 901
!
dial-peer voice 100 voip
 description *** INBOUND FROM PSTN PROVIDER ***
 call-block translation-profile incoming SPAM_CALL_BLOCK
 call-block disconnect-cause incoming call-reject
```

See [`cisco/cube/README_CUBE.md`](cisco/cube/README_CUBE.md).

## Cisco CVP / ICM / UCCE option

For dynamic routing decisions, call the API from CVP Call Studio or an ICM/Cisco CCE Application Gateway integration.

Example CVP/ICM logic:

```text
Get ANI from Call.CallingLineID
Call ANI Risk Validation API
If decision == BLOCK      -> play spam treatment / disconnect after review
If decision == SPAM_QUEUE -> route to special queue
If decision == CHALLENGE  -> IVR verification
If decision == WATCH      -> tag call and route normally
Else                      -> route normally
```

See [`cisco/cvp_icm/README_CVP_ICM.md`](cisco/cvp_icm/README_CVP_ICM.md).

## Repository safety checklist

Before publishing:

- [ ] No `.env` file committed
- [ ] No API keys or tokens
- [ ] No customer call records
- [ ] No internal company ANI list
- [ ] No U-Haul or employer-specific names in data
- [ ] No internal hostnames, IPs, SIP trunks, or dial-peer IDs unless sanitized
- [ ] Only dummy sample data under `data/samples/`
- [ ] MIT license included
- [ ] README explains how to use the project

## Suggested GitHub description

```text
Source-agnostic ANI risk validation toolkit for anti-spam and robocall mitigation in Cisco CUBE, CVP, ICM, and UCCE environments.
```

## Cisco DevNet Code Exchange fit

This project is relevant to Cisco technologies because it includes Cisco CUBE configuration export and Cisco CVP/ICM/UCCE integration design. Keep the repository public, licensed, and well documented before submission.

## References

- Cisco. "Configure Number Translation with Voice Translation Profiles." Cisco Support.
- Cisco. "User Guide for Unified CVP VXML Server and Unified CVP Call Studio: Web Service Integration." Cisco Documentation.
- Cisco DevNet. "Code Exchange." Cisco Developer.
- GitHub Docs. "Adding Locally Hosted Code to GitHub."
