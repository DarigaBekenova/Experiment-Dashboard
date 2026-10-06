from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from .models import Experiment
from .schemas import ExperimentCreate, ExperimentUpdate

ALLOWED_SORT = {"created_at", "name", "accuracy", "duration_sec", "id"}


def list_experiments(
    session: Session,
    q: str | None = None,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> list[Experiment]:
    if sort_by not in ALLOWED_SORT:
        sort_by = "created_at"
    column = getattr(Experiment, sort_by)
    order = column.desc() if sort_order == "desc" else column.asc()
    stmt = select(Experiment).order_by(order, Experiment.id.desc())
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                Experiment.name.ilike(pattern),
                Experiment.dataset.ilike(pattern),
                Experiment.model_name.ilike(pattern),
            )
        )
    if status:
        stmt = stmt.where(Experiment.status == status)
    return list(session.scalars(stmt.limit(limit).offset(offset)))


def get_experiment(session: Session, exp_id: int) -> Experiment | None:
    return session.get(Experiment, exp_id)


def create_experiment(session: Session, data: ExperimentCreate) -> Experiment:
    exp = Experiment(**data.model_dump())
    session.add(exp)
    session.commit()
    session.refresh(exp)
    return exp


def update_experiment(session: Session, exp: Experiment, data: ExperimentUpdate) -> Experiment:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)
    session.commit()
    session.refresh(exp)
    return exp


def delete_experiment(session: Session, exp: Experiment) -> None:
    session.delete(exp)
    session.commit()


def get_stats(session: Session) -> dict:
    total = session.scalar(select(func.count(Experiment.id))) or 0
    rows = list(
        session.execute(select(Experiment.status, func.count()).group_by(Experiment.status))
    )
    by_status = {status: count for status, count in rows}
    avg_acc = session.scalar(select(func.avg(Experiment.accuracy)))
    best = session.scalars(
        select(Experiment).order_by(Experiment.accuracy.desc().nulls_last()).limit(1)
    ).first()
    return {
        "total": total,
        "by_status": by_status,
        "avg_accuracy": float(avg_acc) if avg_acc is not None else None,
        "best_id": best.id if best and best.accuracy is not None else None,
        "best_accuracy": float(best.accuracy) if best and best.accuracy is not None else None,
    }
