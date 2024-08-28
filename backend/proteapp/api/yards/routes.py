from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.yards.schemas import ListedYard, EditableYard, CompleteYard
from proteapp.models.sql.yards import Yard
from proteapp.api.yards_order.schemas import EditableYardOrder
from sqlmodel import Session, select
from proteapp.api.deps import get_sql_session
from proteapp.api.yards_order.routes import post_yard_order, list_yards_order
from ulid import ULID
from datetime import datetime

router = APIRouter(prefix="/yard", tags=["yard"])


@router.get("/search", response_model=list[ListedYard])
def get_yards(session: Session = Depends(get_sql_session)):
    yards = session.exec(select(Yard)).all()
    return yards


@router.post("/", response_model=CompleteYard, status_code=201)
async def post_yard(yard: EditableYard, session: Session = Depends(get_sql_session)):
    yard_db = Yard.model_validate(yard)

    session.add(yard_db)
    session.commit()
    session.refresh(yard_db)

    yard_orders = await list_yards_order()

    if not yard_orders:
        raise HTTPException(status_code=404, detail="No yard orders found")

    closest_yard_order = max(yard_orders, key=lambda order: order.date)

    last_yard_order_ids = [item.id for item in closest_yard_order.yard_order]
    last_yard_order_ids += [yard_db.id]

    newYardOrder = EditableYardOrder(date=datetime.now(), yard_order=last_yard_order_ids)
    await post_yard_order(newYardOrder)

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
async def delete_yard(id: ULID, session: Session = Depends(get_sql_session)):
    yard_db = session.get(Yard, id)

    if yard_db is None:
        raise HTTPException(404, "No yard found")

    session.delete(yard_db)
    session.commit()

    yard_orders = await list_yards_order()

    if not yard_orders:
        raise HTTPException(status_code=404, detail="No yard orders found")

    closest_yard_order = max(yard_orders, key=lambda order: order.date)

    last_yard_order_ids = [item.id for item in closest_yard_order.yard_order]
    last_yard_order_ids.remove(yard_db.id)
    newYardOrder = EditableYardOrder(date=datetime.now(), yard_order=last_yard_order_ids)
    await post_yard_order(newYardOrder)
