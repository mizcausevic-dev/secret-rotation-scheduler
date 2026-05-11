from pydantic import BaseModel, Field


class SecretRecord(BaseModel):
    id: str
    system: str
    owner_lane: str
    environment: str
    secret_type: str
    rotation_window_days: int
    days_since_rotation: int
    expires_in_days: int
    is_break_glass: bool
    has_backup_owner: bool
    last_rotation_actor: str
    next_steps: list[str]
    blockers: list[str]


class DashboardSummary(BaseModel):
    service: str
    tracked_secrets: int
    expiring_soon: int
    stale_rotations: int
    break_glass_exposure: int
    dominant_risk: str
    busiest_lane: str


class SecretCollection(BaseModel):
    secrets: list[SecretRecord]


class RotationAnalysisRequest(BaseModel):
    id: str
    system: str
    owner_lane: str
    environment: str
    secret_type: str
    rotation_window_days: int
    days_since_rotation: int
    expires_in_days: int
    is_break_glass: bool
    has_backup_owner: bool
    last_rotation_actor: str
    next_steps: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)


class RotationAnalysis(BaseModel):
    status: str
    score: int
    rotation_decision: str
    recommended_lane: str
    immediate_action: str
    risks: list[str]
    stabilizers: list[str]
