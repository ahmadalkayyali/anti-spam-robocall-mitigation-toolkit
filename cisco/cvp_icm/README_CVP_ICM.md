# Cisco CVP / ICM / UCCE ANI Validation

This design allows Cisco CVP, ICM, or UCCE routing logic to validate the inbound ANI against the local Anti-Spam and Robocall Mitigation API before the call is queued.

## High-level flow

```text
Inbound Call
   |
   v
Cisco CUBE
   |
   v
CVP / ICM Script
   |
   v
ANI Risk Validation API
   |
   v
Decision returned to routing logic
   |
   +--> ALLOW: route normally
   +--> WATCH: route normally and tag call
   +--> CHALLENGE: send to IVR verification
   +--> SPAM_QUEUE: route to special queue
   +--> BLOCK: controlled treatment/disconnect after review
```

## API request example

```http
GET http://ani-risk-api.local:8080/api/v1/validate?ani=+15551234567&dnis=18005550100&source=cvp
```

## API response example

```json
{
  "ani": "+15551234567",
  "normalized_ani": "+15551234567",
  "dnis": "18005550100",
  "source": "cvp",
  "risk_score": 95,
  "decision": "BLOCK",
  "reason": "Repeated robocall pattern in enterprise contact center",
  "source_hits": ["InternalSpamList"],
  "matched_records": 1,
  "recommended_action": "Reject, disconnect, or route to controlled spam treatment after operational review"
}
```

## ICM routing logic example

```text
Set ANI = Call.CallingLineID
Send to VRU
Run External Script / Call Studio app: ANI_Risk_Check

IF Decision == "BLOCK"
    -> Route to spam treatment or disconnect path after review
ELSE IF Decision == "SPAM_QUEUE"
    -> Queue to special handling skill group
ELSE IF Decision == "CHALLENGE"
    -> Play IVR verification prompt
ELSE IF Decision == "WATCH"
    -> Set PeripheralVariable10 = "ANI_WATCH"
    -> Queue normally
ELSE
    -> Queue normally
```

## CVP Call Studio REST client mapping

Use the Call Studio REST client to call the local API. Store the returned decision in session data, then return a compact value back to ICM, such as:

```text
BLOCK|95|InternalSpamList
ALLOW|0|NoMatch
CHALLENGE|55|TwilioLookup
```

Keep the response compact if passing it through ICM variables.

## Engineering guidance

- Keep the API local or close to the contact center environment.
- Set short timeouts, such as 300-800 ms.
- If the API is unavailable, fail open to normal routing unless your business approves a different behavior.
- Log decisions for reporting and false-positive review.
- Do not block based on a single weak indicator.
