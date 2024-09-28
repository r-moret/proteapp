from proteapp.api.informs.schemas import EditableInform
from proteapp.models.nosql.inform import Inform
from proteapp.models.sql.users import User
from proteapp.models.sql.animals import Animal
from proteapp.models.nosql.yard_order import YardOrder
from proteapp.api.deps import sql_engine
from pydantic import ValidationError
from sqlmodel import Session
from datetime import datetime


async def to_inform(data: EditableInform) -> Inform:
    with Session(sql_engine) as session:
        yard_order = await YardOrder.get(data.yard_order)

        if not yard_order:
            raise ValidationError("Yard order is mandatory")

        return Inform.model_validate(
            {
                **data.model_dump(),
                "date": data.date if not isinstance(data.date, datetime) else data.date.date(),
                "creator": (
                    {
                        **user.model_dump(),
                        "person": user.person.model_dump(),
                    }
                    if (user := session.get(User, data.creator))
                    else None
                ),
                "volunteers": [
                    {
                        **user.model_dump(),
                        "person": user.person.model_dump(),
                    }
                    if (user := session.get(User, vol))
                    else None
                    for vol in data.volunteers
                ],
                "yard_order": [dict(yard) for yard in yard_order.yard_order],
                "notes": [
                    Inform.Note(
                        animal=Inform.Animal.model_validate(
                            animal_note.model_dump()
                            if (animal_note := session.get(Animal, note.animal))
                            else None
                        ),
                        yard=Inform.Note.Yard.model_validate(
                            animal_note.yard.model_dump()
                            if animal_note and animal_note.yard
                            else None
                        ),
                        text=note.text,
                    )
                    for note in data.notes
                ],
                "losses": (
                    [
                        Inform.Loss(
                            animal=Inform.Animal.model_validate(
                                animal_loss.model_dump()
                                if (animal_loss := session.get(Animal, loss.animal))
                                else None
                            )
                        )
                        for loss in data.losses
                    ]
                    if data.losses
                    else None
                ),
                "adoptions": (
                    [
                        Inform.Adoption(
                            animal=Inform.Animal.model_validate(
                                animal_adoption.model_dump()
                                if (animal_adoption := session.get(Animal, adoption.animal))
                                else None
                            ),
                            foster=adoption.foster,
                        )
                        for adoption in data.adoptions
                    ]
                    if data.adoptions
                    else None
                ),
                "tested_animals": (
                    [
                        Inform.TestedAnimal(
                            animal=Inform.Animal.model_validate(
                                animal_test.model_dump()
                                if (animal_test := session.get(Animal, test.animal))
                                else None
                            ),
                            compatible=test.compatible,
                        )
                        for test in data.tested_animals
                    ]
                    if data.tested_animals
                    else None
                ),
            }
        )
