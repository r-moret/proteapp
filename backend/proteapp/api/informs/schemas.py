from proteapp.models.nosql.inform import BaseInform
from beanie import PydanticObjectId


class PublicInform(BaseInform):
    id: PydanticObjectId


class CreateInform(BaseInform): ...


class UpdateInform(BaseInform): ...
