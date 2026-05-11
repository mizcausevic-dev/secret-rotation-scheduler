# Secret Rotation Scheduler

Secret Rotation Scheduler is a Python and FastAPI backend for converting credential age, expiration pressure, and ownership gaps into explicit rotation decisions. It treats secret hygiene as an operating system concern instead of a background checklist.

## Portfolio Takeaway

- Python backend with practical security-hygiene logic
- stale rotation, break-glass exposure, and missing backup ownership turned into concrete action
- JSON API, CLI, tests, docs, and real PNG proof

## Overview

| Area | Details |
| --- | --- |
| Language | Python 3.11+ |
| Framework | FastAPI |
| Focus | Secret rotation scheduling, stale credential detection, backup ownership, expiration pressure |
| Routes | `/`, `/docs`, `/api/dashboard/summary`, `/api/secrets`, `/api/secrets/{id}`, `/api/sample`, `/api/analyze/rotation` |
| Extra | CLI at `python -m app.cli` |

## What It Does

- models secret inventory with owner lanes, expiration windows, and break-glass posture
- scores each payload into `stable`, `watch`, or `escalate`
- returns a rotation decision of `schedule`, `prioritize`, or `rotate-now`
- exposes a JSON API and CLI that can feed runbooks, internal consoles, or reminder workflows

## Architecture

```mermaid
flowchart LR
  A["Secret inventory intake"] --> B["FastAPI routes and CLI"]
  B --> C["Rotation engine"]
  C --> D["Staleness and expiration scoring"]
  C --> E["Owner lane decision"]
  C --> F["Immediate rotation action"]
  D --> G["JSON and CLI output"]
  E --> G
  F --> G
```

Additional detail lives in [C:\Users\chaus\dev\repos\secret-rotation-scheduler\docs\architecture.md](/C:/Users/chaus/dev/repos/secret-rotation-scheduler/docs/architecture.md).

## Example Payload

```json
{
  "id": "sec-7401",
  "system": "billing-export",
  "owner_lane": "platform-security",
  "environment": "prod",
  "secret_type": "api-key",
  "rotation_window_days": 30,
  "days_since_rotation": 43,
  "expires_in_days": 6,
  "is_break_glass": false,
  "has_backup_owner": false,
  "last_rotation_actor": "billing-platform",
  "next_steps": [
    "Assign a backup owner before the next rotation attempt."
  ],
  "blockers": [
    "Rotation runbook still references the legacy export path."
  ]
}
```

## Screenshots

### Hero
![Secret Rotation Scheduler hero](https://raw.githubusercontent.com/mizcausevic-dev/secret-rotation-scheduler/main/screenshots/01-hero.png)

### Queue Lanes
![Secret Rotation Scheduler lanes](https://raw.githubusercontent.com/mizcausevic-dev/secret-rotation-scheduler/main/screenshots/02-lanes.png)

### Rotation Decision
![Secret Rotation Scheduler decision](https://raw.githubusercontent.com/mizcausevic-dev/secret-rotation-scheduler/main/screenshots/03-decision.png)

### Validation Proof
![Secret Rotation Scheduler proof](https://raw.githubusercontent.com/mizcausevic-dev/secret-rotation-scheduler/main/screenshots/04-proof.png)

## Local Run

```powershell
Set-Location "C:\Users\chaus\dev\repos\secret-rotation-scheduler"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 4461
```

Then open:

- `http://127.0.0.1:4461/`
- `http://127.0.0.1:4461/docs`

CLI:

```powershell
.\.venv\Scripts\python.exe -m app.cli
```

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3.11+-0f172a?style=for-the-badge&logo=python&logoColor=f8fafc)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-0f172a?style=for-the-badge&logo=fastapi&logoColor=f8fafc)](https://fastapi.tiangolo.com/)

## Portfolio Links

- [Kinetic Gain](https://kineticgain.com/)
- [LinkedIn](https://www.linkedin.com/in/mirzacausevic)
- [GitHub](https://github.com/mizcausevic-dev)
- [Skills Page](https://mizcausevic.com/skills/)
