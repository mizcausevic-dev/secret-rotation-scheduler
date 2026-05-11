from app.models import RotationAnalysisRequest
from app.services.rotation_engine import analyze, summary


def test_critical_secret_escalates():
    result = analyze(
        RotationAnalysisRequest(
            id="sec-test",
            system="billing-export",
            owner_lane="platform-security",
            environment="prod",
            secret_type="api-key",
            rotation_window_days=30,
            days_since_rotation=45,
            expires_in_days=5,
            is_break_glass=False,
            has_backup_owner=False,
            last_rotation_actor="billing-platform",
            next_steps=["rotate"],
            blockers=["runbook drift"],
        )
    )

    assert result.status == "escalate"
    assert result.rotation_decision == "rotate-now"


def test_summary_counts_inventory():
    result = summary()
    assert result.tracked_secrets == 3
