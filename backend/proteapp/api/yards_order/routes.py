from fastapi import APIRouter, HTTPException, status, Response
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
    except ValidationError:
        raise HTTPException(422, "Unable to create a new yard order with the data passed")

    await yards_order_db.insert()
    return yards_order_db


@router.get(
    "/current",
    response_model=ListedYardOrder,
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def current_yard_order():
    yards_order_db = await YardOrder.find_all().to_list()

    if len(yards_order_db) == 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    date_sorted_yards = sorted(yards_order_db, key=lambda order: order.date)
    return date_sorted_yards[-1]
