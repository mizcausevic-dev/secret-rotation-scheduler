from app.models import SecretRecord


def records() -> list[SecretRecord]:
    return [
        SecretRecord(
            id="sec-7004",
            system="billing-export",
            owner_lane="platform-security",
            environment="prod",
            secret_type="api-key",
            rotation_window_days=30,
            days_since_rotation=43,
            expires_in_days=6,
            is_break_glass=False,
            has_backup_owner=False,
            last_rotation_actor="billing-platform",
            next_steps=[
                "Assign a backup owner before the next rotation attempt.",
                "Rotate the export key before finance close preparation begins.",
            ],
            blockers=[
                "Rotation runbook still references the legacy export path.",
            ],
        ),
        SecretRecord(
            id="sec-7011",
            system="identity-sync",
            owner_lane="identity-systems",
            environment="prod",
            secret_type="certificate",
            rotation_window_days=45,
            days_since_rotation=29,
            expires_in_days=18,
            is_break_glass=True,
            has_backup_owner=True,
            last_rotation_actor="identity-ops",
            next_steps=[
                "Validate the break-glass cert storage path.",
            ],
            blockers=[],
        ),
        SecretRecord(
            id="sec-7018",
            system="feature-delivery",
            owner_lane="growth-systems",
            environment="stage",
            secret_type="token",
            rotation_window_days=21,
            days_since_rotation=19,
            expires_in_days=12,
            is_break_glass=False,
            has_backup_owner=True,
            last_rotation_actor="growth-platform",
            next_steps=[
                "Keep the normal scheduler window and notify the backup owner.",
            ],
            blockers=[],
        ),
    ]
