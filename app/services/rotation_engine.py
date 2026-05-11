from app.models import (
    DashboardSummary,
    RotationAnalysis,
    RotationAnalysisRequest,
    SecretRecord,
)
from app.sample_data import records


def summary() -> DashboardSummary:
    secrets = records()
    return DashboardSummary(
        service="secret-rotation-scheduler",
        tracked_secrets=len(secrets),
        expiring_soon=sum(1 for secret in secrets if secret.expires_in_days <= 14),
        stale_rotations=sum(1 for secret in secrets if secret.days_since_rotation > secret.rotation_window_days),
        break_glass_exposure=sum(1 for secret in secrets if secret.is_break_glass),
        dominant_risk="Unowned production secret approaching expiration",
        busiest_lane="platform-security",
    )


def list_secrets() -> list[SecretRecord]:
    return records()


def get_secret(secret_id: str) -> SecretRecord | None:
    for secret in records():
        if secret.id == secret_id:
            return secret
    return None


def sample_analysis() -> RotationAnalysis:
    secret = records()[0]
    return analyze(
        RotationAnalysisRequest(
            id=secret.id,
            system=secret.system,
            owner_lane=secret.owner_lane,
            environment=secret.environment,
            secret_type=secret.secret_type,
            rotation_window_days=secret.rotation_window_days,
            days_since_rotation=secret.days_since_rotation,
            expires_in_days=secret.expires_in_days,
            is_break_glass=secret.is_break_glass,
            has_backup_owner=secret.has_backup_owner,
            last_rotation_actor=secret.last_rotation_actor,
            next_steps=secret.next_steps,
            blockers=secret.blockers,
        )
    )


def analyze(request: RotationAnalysisRequest) -> RotationAnalysis:
    score = 10

    if request.days_since_rotation > request.rotation_window_days:
        score += 28
    elif request.days_since_rotation >= request.rotation_window_days - 3:
        score += 14

    if request.expires_in_days <= 7:
        score += 26
    elif request.expires_in_days <= 14:
        score += 16

    if request.is_break_glass:
        score += 10

    if not request.has_backup_owner:
        score += 12

    if request.environment.lower() == "prod":
        score += 10

    if request.blockers:
        score += min(12, len(request.blockers) * 6)

    status = "stable"
    if score >= 72:
        status = "escalate"
    elif score >= 46:
        status = "watch"

    rotation_decision = {
        "stable": "schedule",
        "watch": "prioritize",
        "escalate": "rotate-now",
    }[status]

    recommended_lane = "incident-command" if status == "escalate" and not request.has_backup_owner else request.owner_lane

    immediate_action = {
        "stable": "Keep the secret in the normal scheduler lane and notify the backup owner before the next window.",
        "watch": "Pull the secret into the next priority rotation batch and clear any runbook blockers before the expiration buffer tightens.",
        "escalate": "Route the secret into immediate rotation ownership, assign a named backup owner, and freeze dependent deploys until rotation proof is captured.",
    }[status]

    risks: list[str] = []
    if request.days_since_rotation > request.rotation_window_days:
        risks.append("The secret is already beyond its normal rotation window.")
    if request.expires_in_days <= 7:
        risks.append("The secret is approaching expiration inside a one-week window.")
    if not request.has_backup_owner:
        risks.append("There is no backup owner if the primary rotation lane is blocked.")
    if request.is_break_glass:
        risks.append("Break-glass material always carries elevated governance pressure.")
    if request.blockers:
        risks.append("Runbook or path blockers are still attached to the rotation.")

    stabilizers: list[str] = []
    if request.has_backup_owner:
        stabilizers.append("A backup owner already exists.")
    if request.expires_in_days > 14:
        stabilizers.append("The expiration buffer still leaves room for a controlled rotation.")
    if request.next_steps:
        stabilizers.append("A next-step sequence already exists for the owner lane.")

    return RotationAnalysis(
        status=status,
        score=score,
        rotation_decision=rotation_decision,
        recommended_lane=recommended_lane,
        immediate_action=immediate_action,
        risks=risks,
        stabilizers=stabilizers,
    )
