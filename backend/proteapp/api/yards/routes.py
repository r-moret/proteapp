from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.yards.schemas import (
    PublicYardWithRelationships,
    CreateYard,
    PublicYard,
    UpdateYard,
)
from proteapp.models.yards import Yard
from sqlmodel import Session, select
from proteapp.api.deps import get_session

router = APIRouter(prefix="/yard", tags=["yard"])


@router.get("/search", response_model=list[PublicYardWithRelationships])
def get_yards(session: Session = Depends(get_session)):
    yards = session.exec(select(Yard)).all()
    return yards


@router.post("/", response_model=PublicYard, status_code=201)
def post_yard(yard: CreateYard, session: Session = Depends(get_session)):
    yard_db = Yard.model_validate(yard)

    session.add(yard_db)
    session.commit()
    session.refresh(yard_db)

    return yard_db


@router.get("/{id}", response_model=PublicYardWithRelationships)
def get_yard(id: int, session: Session = Depends(get_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "Yard not found")

    return yard_db


@router.put("/{id}", response_model=PublicYard)
def put_yard(id: int, yard: UpdateYard, session: Session = Depends(get_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "Yard not found")

    yard_db.sqlmodel_update(yard)

    session.add(yard_db)
    session.commit()
    session.refresh(yard_db)

    return yard_db


@router.delete("/{id}")
def delete_yard(id: int, session: Session = Depends(get_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "Yard not found")

    session.delete(yard_db)
    session.commit()
