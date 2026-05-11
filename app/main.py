from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.models import RotationAnalysisRequest, SecretCollection
from app.services import rotation_engine

app = FastAPI(
    title="secret-rotation-scheduler",
    docs_url=None,
    redoc_url=None,
)


@app.get("/")
def root() -> dict:
    return {
        "service": "secret-rotation-scheduler",
        "language": "Python",
        "framework": "FastAPI",
        "description": "Secret rotation and stale credential control for production, break-glass, and owner-reminder workflows.",
        "endpoints": [
            "/docs",
            "/api/dashboard/summary",
            "/api/secrets",
            "/api/secrets/{id}",
            "/api/sample",
            "/api/analyze/rotation",
        ],
    }


@app.get("/docs", response_class=HTMLResponse)
def docs() -> str:
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>Secret Rotation Scheduler Docs</title>
        <style>
          body { font-family: Segoe UI, sans-serif; background:#09121f; color:#f3efe1; margin:0; padding:32px; }
          .shell { max-width:960px; margin:0 auto; background:#131d30; border:1px solid #294164; border-radius:20px; padding:28px; }
          h1 { margin:0 0 8px; font-size:40px; line-height:1.08; }
          p, li, code { color:#c6d0e2; }
          code { background:#0d1728; padding:2px 6px; border-radius:6px; }
        </style>
      </head>
      <body>
        <div class="shell">
          <p style="letter-spacing:0.25em;text-transform:uppercase;color:#86c4ff;">Secret Rotation Scheduler</p>
          <h1>Python control surface for stale secrets, rotation windows, and owner-aware security hygiene.</h1>
          <p>This service turns credential decay into explicit rotation decisions instead of leaving it trapped in ticket queues and spreadsheets.</p>
          <ul>
            <li><code>GET /api/dashboard/summary</code> returns queue posture.</li>
            <li><code>GET /api/secrets</code> returns the modeled secret inventory.</li>
            <li><code>GET /api/sample</code> returns a sample rotation analysis.</li>
            <li><code>POST /api/analyze/rotation</code> scores a payload and returns the next action.</li>
          </ul>
        </div>
      </body>
    </html>
    """


@app.get("/api/dashboard/summary")
def dashboard_summary():
    return rotation_engine.summary()


@app.get("/api/secrets")
def secrets() -> SecretCollection:
    return SecretCollection(secrets=rotation_engine.list_secrets())


@app.get("/api/secrets/{secret_id}")
def secret(secret_id: str):
    found = rotation_engine.get_secret(secret_id)
    if found is None:
        raise HTTPException(status_code=404, detail={"error": "secret_not_found", "id": secret_id})
    return found


@app.get("/api/sample")
def sample():
    return rotation_engine.sample_analysis()


@app.post("/api/analyze/rotation")
def analyze(payload: RotationAnalysisRequest):
    return rotation_engine.analyze(payload)
