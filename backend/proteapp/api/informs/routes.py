from fastapi import APIRouter, HTTPException, Depends
from proteapp.api.informs.schemas import (
    CompleteInform,
    ListedInform,
    EditableInform,
)
from proteapp.models.nosql.inform import Inform
from ulid import ULID
from proteapp.api.informs.adapters import to_inform
from pydantic import ValidationError
from proteapp.api.deps import admin_required

router = APIRouter(prefix="/inform", tags=["inform"])


@router.get("/search", response_model=list[ListedInform])
async def list_informs():
    informs_db = await Inform.find_all().to_list()
    return informs_db


@router.post("/", response_model=CompleteInform, status_code=201)
async def create_inform(inform: EditableInform):
    try:
        inform_db = await to_inform(inform)
    except ValidationError:
        raise HTTPException(422, "Unable to create a new inform with the data passed")

    await inform_db.insert()
    return inform_db


@router.get("/{id}", response_model=CompleteInform)
async def get_inform(id: ULID):
    inform_db = await Inform.get(id)

    if not inform_db:
        raise HTTPException(404, "Inform not found")

    return inform_db


@router.put("/{id}", response_model=CompleteInform)
async def update_inform(id: ULID, inform: EditableInform):
    inform_db = await Inform.get(id)

    if not inform_db:
        raise HTTPException(404, "Inform not found")

    try:
        changed_inform = await to_inform(inform)
    except ValidationError:
        raise HTTPException(422, "Unable to update the inform with the data passed")

    for prop, value in dict(changed_inform).items():
        if prop == "id":
            continue

        setattr(inform_db, prop, value)

    await inform_db.replace()
    return inform_db


@router.delete("/{id}", dependencies=[Depends(admin_required)])
async def delete_inform(id: ULID):
    inform_db = await Inform.get(id)

    if not inform_db:
        raise HTTPException(404, "Inform not found")

    await inform_db.delete()
