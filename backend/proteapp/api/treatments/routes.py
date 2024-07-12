from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.deps import get_session
from proteapp.models.animals import Animal
from proteapp.api.treatments.schemas import CreateTreatment, PublicTreatment
from proteapp.models.treatments import Treatment
from sqlmodel import Session, select

router = APIRouter(prefix="/treatment", tags=["treatment"])


@router.get("/search", response_model=list[PublicTreatment])
def get_treatments(session: Session = Depends(get_session)):
    return session.exec(select(Treatment)).all()


@router.post("/", response_model=PublicTreatment, status_code=201)
def post_treatment(treatment: CreateTreatment, session: Session = Depends(get_session)):
    treatment_db = Treatment.model_validate(treatment)

    animal_db = session.get(Animal, treatment.animal_id)

    if not animal_db:
        raise HTTPException(404, "No animal found")

    animal_db.treatments.append(treatment_db)

    session.add(animal_db)
    session.commit()
    session.refresh(treatment_db)

    return treatment_db


@router.delete("/{id}")
def delete_treatment(id: int, session: Session = Depends(get_session)):
    treatment_db = session.get(Treatment, id)

    if treatment_db is None:
        raise HTTPException(404, "No animal found")

    session.delete(treatment_db)
    session.commit()