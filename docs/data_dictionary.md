# Data Dictionary

## `ani_risk_sources`

| Field | Type | Description |
|---|---|---|
| `id` | integer | Local primary key |
| `ani` | text | Raw ANI as imported |
| `normalized_ani` | text | Normalized ANI used for matching |
| `source_name` | text | Name of the source, such as `InternalSpamList`, `CarrierDNO`, or `TwilioLookup` |
| `source_type` | text | Category such as `internal`, `dno`, `complaints`, `enrichment`, `public_reference`, or `custom` |
| `risk_level` | text | `info`, `low`, `medium`, `high`, or `critical` |
| `risk_score` | integer | Numeric score from 0 to 100 |
| `reason` | text | Human-readable reason for the record |
| `first_seen` | text | First date observed, if known |
| `last_seen` | text | Last date observed, if known |
| `active` | integer | 1 means active; 0 means ignored/disabled |
| `notes` | text | Safe notes. Do not place secrets or customer data here. |

## `validation_log`

| Field | Type | Description |
|---|---|---|
| `id` | integer | Local primary key |
| `ani` | text | Raw queried ANI |
| `normalized_ani` | text | Normalized ANI |
| `dnis` | text | Optional called number |
| `source` | text | Caller of API, such as `cvp`, `icm`, `cli`, or `batch` |
| `decision` | text | Returned decision |
| `risk_score` | integer | Returned risk score |
| `created_at` | text | Timestamp of lookup |
