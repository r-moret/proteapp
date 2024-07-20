from proteapp.api.informs.schemas import EditableInform
from proteapp.models.nosql.inform import Inform
from proteapp.models.sql.people import Person
from proteapp.models.sql.animals import Animal
from proteapp.api.deps import sql_engine
from sqlmodel import Session


def to_inform(data: EditableInform) -> Inform:
    with Session(sql_engine) as session:
        return Inform.model_validate(
            {
                **data.model_dump(),
                "creator": (
                    person.model_dump() if (person := session.get(Person, data.creator)) else None
                ),
                "volunteers": [
                    person.model_dump() if (person := session.get(Person, vol)) else None
                    for vol in data.volunteers
                ],
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
