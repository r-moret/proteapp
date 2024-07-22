from fastapi import APIRouter, Depends
from proteapp.api.deps import get_sql_session
from sqlmodel import Session, select
from proteapp.api.adoptions.schemas import ListedAdoption
from proteapp.models.sql.adoptions import Adoption

router = APIRouter(prefix="/adoptions", tags=["adoptions"])


@router.get("/search", response_model=list[ListedAdoption])
def list_adoptions(session: Session = Depends(get_sql_session)):
    adoptions = session.exec(select(Adoption)).all()
    return adoptions
