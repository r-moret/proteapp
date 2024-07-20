from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.deps import get_sql_session
from proteapp.api.treatments.schemas import EditableTreatment, CompleteTreatment
from proteapp.models.sql.treatments import Treatment
from sqlmodel import Session
from proteapp.api.treatments.adapters import to_treatment
from ulid import ULID
from pydantic import ValidationError

router = APIRouter(prefix="/treatment", tags=["treatment"])


@router.post("/", response_model=CompleteTreatment, status_code=201)
def create_treatment(treatment: EditableTreatment, session: Session = Depends(get_sql_session)):
    try:
        treatment_db = to_treatment(treatment)
    except ValidationError:
        raise HTTPException(422, "Unable to create new treatment with the data passed")

    session.add(treatment_db)
    session.commit()
    session.refresh(treatment_db)

    return treatment_db


@router.delete("/{id}", status_code=204)
def delete_treatment(id: ULID, session: Session = Depends(get_sql_session)):
    treatment_db = session.get(Treatment, id)

    if treatment_db is None:
        raise HTTPException(404, "No treatment found")

    session.delete(treatment_db)
    session.commit()
