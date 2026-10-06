from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_session

from . import service
from .models import Experiment
from .schemas import ExperimentCreate, ExperimentOut, ExperimentStats, ExperimentUpdate

router = APIRouter(prefix="/experiments", tags=["experiments"])


def get_or_404(exp_id: int, session: Session = Depends(get_session)) -> Experiment:
    exp = service.get_experiment(session, exp_id)
    if exp is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Experiment not found")
    return exp


@router.get("/stats", response_model=ExperimentStats)
def experiment_stats(session: Session = Depends(get_session)):
    return service.get_stats(session)


@router.get("", response_model=list[ExperimentOut])
def list_experiments(
    q: str | None = Query(default=None, max_length=200),
    status: str | None = Query(default=None, pattern="^(planned|running|completed|failed)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    session: Session = Depends(get_session),
):
    return service.list_experiments(session, q, status, limit, offset, sort_by, sort_order)


@router.get("/{exp_id}", response_model=ExperimentOut)
def read_experiment(exp: Experiment = Depends(get_or_404)):
    return exp


@router.post("", response_model=ExperimentOut, status_code=status.HTTP_201_CREATED)
def create_experiment(data: ExperimentCreate, session: Session = Depends(get_session)):
    return service.create_experiment(session, data)


@router.patch("/{exp_id}", response_model=ExperimentOut)
def update_experiment(
    data: ExperimentUpdate,
    exp: Experiment = Depends(get_or_404),
    session: Session = Depends(get_session),
):
    return service.update_experiment(session, exp, data)


@router.delete("/{exp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiment(
    exp: Experiment = Depends(get_or_404), session: Session = Depends(get_session)
) -> None:
    service.delete_experiment(session, exp)
