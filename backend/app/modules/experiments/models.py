from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

STATUS_PLANNED = "planned"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

ALLOWED_STATUSES = {STATUS_PLANNED, STATUS_RUNNING, STATUS_COMPLETED, STATUS_FAILED}


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500), index=True)
    dataset: Mapped[str] = mapped_column(String(500), index=True)
    model_name: Mapped[str] = mapped_column(String(500), index=True)
    status: Mapped[str] = mapped_column(String(50), default=STATUS_PLANNED, index=True)
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
