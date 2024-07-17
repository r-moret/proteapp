from fastapi import APIRouter, HTTPException
from proteapp.api.informs.schemas import PublicInform, CreateInform, UpdateInform
from proteapp.models.nosql.inform import Inform
from beanie import PydanticObjectId

router = APIRouter(prefix="/inform", tags=["inform"])


@router.get("/search", response_model=list[PublicInform])
async def list_informs():
    informs = await Inform.find_all().to_list()
    return informs


@router.post("/", response_model=PublicInform, status_code=201)
async def create_inform(inform: CreateInform):
    inform_db = Inform(**inform.model_dump())

    await inform_db.insert()
    return inform_db


@router.get("/{id}", response_model=PublicInform)
async def get_inform(id: PydanticObjectId):
    inform_db = await Inform.get(id)

    if not inform_db:
        raise HTTPException(404, "Inform not found")

    return inform_db


@router.put("/{id}", response_model=PublicInform)
async def update_inform(id: PydanticObjectId, inform: UpdateInform):
    inform_db = await Inform.get(id)

    if not inform_db:
        raise HTTPException(404, "Inform not found")

    for prop, value in inform.model_dump().items():
        setattr(inform_db, prop, value)

    await inform_db.replace()

    return inform_db


@router.delete("/{id}")
async def delete_inform(id: PydanticObjectId):
    inform_db = await Inform.get(id)

    if not inform_db:
        raise HTTPException(404, "Inform not found")

    await inform_db.delete()
