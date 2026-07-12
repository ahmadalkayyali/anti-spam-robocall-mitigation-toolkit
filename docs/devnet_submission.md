# Cisco DevNet Code Exchange Submission Draft

## Project title

Anti-Spam and Robocall Mitigation Toolkit

## Short description

Source-agnostic ANI risk validation toolkit for anti-spam and robocall mitigation in Cisco CUBE, CVP, ICM, and UCCE environments.

## Long description

This project provides a reusable ANI risk validation framework for Cisco voice and contact center environments. It allows engineers to validate inbound caller ANI values against trusted spam, robocall, DNO, carrier, internal complaint, and custom risk datasets before the call is routed.

The toolkit includes a local SQLite database builder, a FastAPI validation service, sample Cisco CVP/ICM routing logic, and a Cisco CUBE call-block configuration generator for reviewed high-risk ANI values.

## Cisco technologies

- Cisco CUBE
- Cisco CVP
- Cisco ICM
- Cisco UCCE / Packaged CCE
- Cisco CUCM
- SIP trunking

## Tags

`cisco-cube`, `cvp`, `icm`, `ucce`, `contact-center`, `voice`, `sip`, `robocall`, `spam`, `ani-validation`, `security`, `automation`

## Demo steps

```bash
pip install -r requirements.txt
python scripts/build_db.py --source data/samples/ani_risk_sources_sample.csv --db data/output/ani_risk.sqlite
python scripts/query_ani.py --ani +15551234567 --db data/output/ani_risk.sqlite
python scripts/generate_cube_blocklist.py --input data/samples/ani_risk_sources_sample.csv --output data/output/cube_spam_blocklist.cfg
uvicorn antispam_robocall_toolkit.api:app --app-dir src --reload --port 8080
```

## Public data statement

This repository includes dummy data only. Production ANI intelligence should remain private unless the data owner explicitly authorizes publication.
