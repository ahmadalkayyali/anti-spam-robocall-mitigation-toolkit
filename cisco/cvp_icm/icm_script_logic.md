# Sample ICM Script Logic

```text
Start
  |
  v
Set Variable: Call.PeripheralVariable1 = Call.CallingLineID
  |
  v
Send To VRU
  |
  v
Run External Script: ANI_Risk_Check
  |
  v
Decision Node:
  - Contains "BLOCK"      -> Spam_Block_Treatment
  - Contains "SPAM_QUEUE" -> Spam_Review_Skill_Group
  - Contains "CHALLENGE"  -> Verification_IVR
  - Contains "WATCH"      -> Normal route + reporting tag
  - Else                  -> Normal route
```

Suggested variables:

| Variable | Purpose |
|---|---|
| `Call.CallingLineID` | Raw inbound ANI |
| `Call.DialedNumberString` | DNIS/called number |
| `user.microapp.caller_input` | Compact returned decision if using microapp pattern |
| `Call.PeripheralVariable10` | Optional reporting tag such as `ANI_WATCH` |
