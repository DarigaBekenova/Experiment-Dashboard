from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["planned", "running", "completed", "failed"]


class ExperimentBase(BaseModel):
    name: str = Field(min_length=3, max_length=500)
    dataset: str = Field(min_length=2, max_length=500)
    model_name: str = Field(min_length=2, max_length=500)
    status: Status = "planned"
    accuracy: float | None = Field(default=None, ge=0, le=1)
    duration_sec: float | None = Field(default=None, ge=0)
    notes: str | None = None


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=500)
    dataset: str | None = Field(default=None, min_length=2, max_length=500)
    model_name: str | None = Field(default=None, min_length=2, max_length=500)
    status: Status | None = None
    accuracy: float | None = Field(default=None, ge=0, le=1)
    duration_sec: float | None = Field(default=None, ge=0)
    notes: str | None = None


class ExperimentOut(ExperimentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ExperimentStats(BaseModel):
    total: int
    by_status: dict[str, int]
    avg_accuracy: float | None
    best_id: int | None
    best_accuracy: float | None
