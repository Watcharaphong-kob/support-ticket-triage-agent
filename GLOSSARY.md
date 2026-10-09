# Support Ticket Triage

Language for interpreting the original assignment and customer conversations.

## Language

**Ticket**:
A customer support case containing the supplied customer context and the full conversation about unresolved issues.
_Avoid_: A single message, chat session

**Message**:
One contribution in a ticket conversation, retaining its original wording, order and supplied relative time.
_Avoid_: Summary, triage decision

**Customer report**:
A claim made by the customer, which can justify investigation without establishing that the claimed payment state or incident is confirmed.
_Avoid_: Verified fact, confirmed incident

**Customer history**:
The available account and prior-support context associated with a customer.
_Avoid_: Verified payment ledger, live account state

**Knowledge article**:
A source FAQ or document containing information relevant to a support issue.
_Avoid_: Agent instruction, customer history

**Mock knowledge**:
Illustrative FAQ or document content used for a demonstration, with no authority to establish actual company policies or incident status.
_Avoid_: Verified company policy, live status

**Citation**:
A reference identifying the retrieved knowledge source supporting a stated answer or explanation.
_Avoid_: Confidence score, proof of a customer report

**Urgency**:
The ticket's critical, high, medium or low level of need for attention, based on reported impact and time sensitivity.
_Avoid_: Customer sentiment, account tier

**Next action**:
The selected response path: auto-respond, route to a specialist, or escalate to a human.
_Avoid_: Urgency, executed account change

**Draft response**:
Proposed customer-facing wording associated with the selected next action.
_Avoid_: Sent message, completed resolution

**Fallback**:
A disclosed inability to complete reliable triage, accompanied by human escalation and the known failure cause.
_Avoid_: Completed triage, no-match
