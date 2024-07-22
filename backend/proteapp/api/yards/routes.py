from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.yards.schemas import ListedYard, EditableYard, CompleteYard
from proteapp.models.sql.yards import Yard
from sqlmodel import Session, select
from proteapp.api.deps import get_sql_session
from ulid import ULID

router = APIRouter(prefix="/yard", tags=["yard"])


@router.get("/search", response_model=list[ListedYard])
def get_yards(session: Session = Depends(get_sql_session)):
    yards = session.exec(select(Yard)).all()
    return yards


@router.post("/", response_model=CompleteYard, status_code=201)
def post_yard(yard: EditableYard, session: Session = Depends(get_sql_session)):
    yard_db = Yard.model_validate(yard)

    session.add(yard_db)
    session.commit()
    session.refresh(yard_db)

    return yard_db


@router.get("/{id}", response_model=CompleteYard)
def get_yard(id: ULID, session: Session = Depends(get_sql_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "No yard found")

    return yard_db


@router.put("/{id}", response_model=CompleteYard)
def put_yard(id: ULID, yard: EditableYard, session: Session = Depends(get_sql_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "No yard found")

    yard_db.sqlmodel_update(yard)

    session.add(yard_db)
    session.commit()
    session.refresh(yard_db)

    return yard_db


@router.delete("/{id}", status_code=204)
def delete_yard(id: ULID, session: Session = Depends(get_sql_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "No yard found")

    session.delete(yard_db)
    session.commit()
