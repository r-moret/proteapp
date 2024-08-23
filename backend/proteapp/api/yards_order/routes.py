from fastapi import APIRouter, HTTPException
from proteapp.api.yards_order.schemas import EditableYardOrder, ListedYardOrder
from proteapp.models.nosql.yard_order import YardOrder
from proteapp.api.yards_order.adapters import to_yard_order

from pydantic import ValidationError

router = APIRouter(prefix="/yard_order", tags=["yard_order"])


@router.get("/search", response_model=list[ListedYardOrder])
async def list_yards_order():
    yards_order_db = await YardOrder.find_all().to_list()
    return yards_order_db


@router.post("/", response_model=ListedYardOrder, status_code=201)
async def post_yard_order(yard_order: EditableYardOrder):
    try:
        yards_order_db = to_yard_order(yard_order)
    except ValidationError as e:
        print(e)
        raise HTTPException(422, "Unable to create a new yard order with the data passed")

    await yards_order_db.insert()
    return yards_order_db
