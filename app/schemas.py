from datetime import datetime

from pydantic import BaseModel


class BugCreate(BaseModel):
    title: str
    description: str | None = None
    severity: str = "medium"
    status: str = "open"


class BugResponse(BaseModel):
    id: int
    title: str
    description: str | None
    severity: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
