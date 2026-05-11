# Secret Rotation Scheduler Architecture

Secret Rotation Scheduler is built as a lightweight Python control layer that turns credential hygiene into an explicit decision. The service is intentionally simple: it should be easy to run, easy to inspect, and easy to route into future security workflows.

## Core Flow

1. A secret record arrives with age, expiration window, owner lane, and break-glass posture.
2. The FastAPI route layer or CLI forwards the payload to the rotation engine.
3. The engine scores staleness, expiration pressure, missing backup ownership, blockers, and break-glass risk.
4. The result becomes a rotation decision:
   - `schedule`
   - `prioritize`
   - `rotate-now`
5. The service returns the owner lane and immediate action.

## Why This Repo Matters

- it expands the portfolio’s security operations layer
- it keeps the Python signal practical, not academic
- it complements governance, tenant isolation, and compliance work already in the repo graph
