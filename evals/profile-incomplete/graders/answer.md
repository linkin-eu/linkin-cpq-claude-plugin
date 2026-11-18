---
type: llm
---

PASS if the reply says LINKIN couldn't price the inquiry because the LINKIN account's profile lacks the phone number, and sends the buyer to complete the profile at https://linkin.eu/en/complete-profile/ before asking again.
FAIL if it gives a price, says an inquiry was issued, names a missing detail other than the phone number, asks the buyer to give their phone number or other details in the conversation, or says it will retry without the profile being completed.
