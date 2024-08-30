from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.deps import get_sql_session, admin_required
from proteapp.exceptions import UnsavedDataError
from pydantic import ValidationError
from sqlmodel import Session, select
from proteapp.api.adoptions.schemas import ListedAdoption, CompleteAdoption, EditableAdoption
from proteapp.api.adoptions.adapters import to_adoption
from proteapp.models.sql.adoptions import Adoption
from ulid import ULID

router = APIRouter(prefix="/adoption", tags=["adoption"])


@router.get("/search", response_model=list[ListedAdoption])
def list_adoptions(session: Session = Depends(get_sql_session)):
    adoptions = session.exec(select(Adoption)).all()
    return adoptions


@router.get("/{id}", response_model=CompleteAdoption)
def get_adoption(id: ULID, session: Session = Depends(get_sql_session)):
    adoption_db = session.get(Adoption, id)

    if adoption_db is None:
        raise HTTPException(404, "No adoption found")

    return adoption_db


@router.delete("/{id}", status_code=204, dependencies=[Depends(admin_required)])
def delete_adoption(id: ULID, session: Session = Depends(get_sql_session)):
    adoption_db = session.get(Adoption, id)

    if adoption_db is None:
        raise HTTPException(404, "No adoption found")

    session.delete(adoption_db)
    session.commit()


@router.post("/", response_model=CompleteAdoption, status_code=201)
def post_adoption(adoption: EditableAdoption, session: Session = Depends(get_sql_session)):
    try:
        adoption_db = to_adoption(adoption)
    except UnsavedDataError as e:
        raise HTTPException(
            422, f'The field "{e.field}" makes reference to an entity that is not saved yet'
        )
    except ValidationError:
        raise HTTPException(422, "Unable to create an adoption with the data passed")

    session.add(adoption_db)
    session.commit()
    session.refresh(adoption_db)

    return adoption_db
