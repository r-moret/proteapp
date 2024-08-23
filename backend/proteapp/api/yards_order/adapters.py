from proteapp.api.yards_order.schemas import EditableYardOrder
from proteapp.models.nosql.yard_order import YardOrder
from proteapp.models.sql.yards import Yard
from proteapp.exceptions import UnsavedDataError
from proteapp.api.deps import sql_engine
from sqlmodel import Session


def to_yard_order(data: EditableYardOrder) -> YardOrder:
    with Session(sql_engine) as session:
        valid_yard_order = [
            dict(yard) if (yard := session.get(Yard, yard_value)) else None
            for yard_value in data.yard_order
        ]

        if not all(valid_yard_order):
            raise UnsavedDataError(
                "Cannot create a yard order with non-existing yards", field="yard_order"
            )

        return YardOrder.model_validate({"date": data.date, "yard_order": valid_yard_order})
