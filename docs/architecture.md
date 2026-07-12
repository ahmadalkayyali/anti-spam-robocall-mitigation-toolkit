# Architecture

## Source-agnostic data model

The toolkit does not depend on one specific spam or robocall database. It uses a normalized local table called `ani_risk_sources`.

```text
Any trusted ANI source
  |
  +--> CSV import
  +--> API enrichment
  +--> Manual review list
  +--> Carrier/DNO feed
  |
  v
ani_risk_sources table
  |
  v
Validation API / reporting / CUBE export / CVP-ICM routing decision
```

## Real-time routing model

```text
Carrier SIP Trunk
   |
   v
Cisco CUBE
   |
   v
Cisco CVP / ICM / UCCE
   |
   v
ANI Risk Validation API
   |
   v
Local SQLite or enterprise database
```

The API returns a compact decision that routing logic can consume.

## Static blocking model

```text
Reviewed high-risk ANI records
   |
   v
CUBE call-block config generator
   |
   v
Cisco CUBE inbound dial-peer
```

Static blocking should be used only for confirmed high-risk numbers and after operational review.
