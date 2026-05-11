from app.sample_data import records
from app.services.rotation_engine import analyze
from app.models import RotationAnalysisRequest


def main() -> None:
    print("Secret Rotation Scheduler")
    print("=========================")
    for secret in records():
        result = analyze(
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
        print(f"{secret.id}: {result.rotation_decision} ({result.status}) -> {result.recommended_lane}")


if __name__ == "__main__":
    main()
