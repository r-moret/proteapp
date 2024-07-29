from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.deps import get_sql_session
from proteapp.api.monitorings.schemas import EditableMonitoring, CompleteMonitoring
from proteapp.models.sql.monitorings import Monitoring
from sqlmodel import Session
from ulid import ULID
from proteapp.api.monitorings.adapters import to_monitoring
from proteapp.exceptions import UnsavedDataError
from pydantic import ValidationError

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.post("/", response_model=CompleteMonitoring, status_code=201)
def post_monitoring(monitoring: EditableMonitoring, session: Session = Depends(get_sql_session)):
    try:
        monitoring_db = to_monitoring(monitoring)
    except UnsavedDataError as e:
        raise HTTPException(
            422, f'The field "{e.field}" makes reference to an entity that is not saved yet'
        )
    except ValidationError:
        raise HTTPException(422, "Unable to create an monitoring with the data passed")

    session.add(monitoring_db)
    session.commit()
    session.refresh(monitoring_db)

    return monitoring_db


@router.delete("/{id}", status_code=204)
def delete_monitoring(id: ULID, session: Session = Depends(get_sql_session)):
    monitoring_db = session.get(Monitoring, id)

    if monitoring_db is None:
        raise HTTPException(404, "No monitoring found")

    session.delete(monitoring_db)
    session.commit()
