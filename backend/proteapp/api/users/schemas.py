from proteapp.models.users import BaseUser

class CreateUser(BaseUser): ...


class PublicUser(BaseUser):
    id: int

