from proteapp.api.deps import get_sql_session
from proteapp.models.nosql.inform import Inform
from proteapp.models.sql.animals import Animal, Sex
from datetime import datetime
from typing import cast
from ulid import ULID

from proteapp.models.sql.treatments import Treatment
from proteapp.models.sql.appointments import Appointment
from proteapp.models.sql.yards import Yard
from proteapp.models.sql.users import User
from proteapp.models.sql.people import Person, PhoneNumber

people = [
    Person(
        name="Cris",
        first_surname="Espejo",
        email="cris@espejo.com",
        phone=PhoneNumber("+34640040545"),
        user=User(
            id=ULID.from_str("01J3DSAAMJCCXJNB7M2XZGVEPW"),  # Fixed, this is the fake logged user
            active=True,
            veteran=True,
            password="hola",
        ),
    ),
    Person(
        name="Rafael",
        first_surname="Moret",
        email="rafa@moret.com",
        phone=PhoneNumber("+34640564432"),
        user=User(active=True, veteran=False, password="adios"),
    ),
]

yards = [
    Yard(name="Patio 1"),
    Yard(name="Patio 2"),
    Yard(name="Patio inmunodeficiencia"),
]

animals = [
    Animal(
        name="Carolina",
        description="Carolina es una hermosa gata con un pelaje suave y lujoso. Disfruta tomando el sol y acurrucándose con sus compañeros humanos. A pesar de su apariencia regia, Carolina es increíblemente amigable y le encanta conocer gente nueva y otros animales.",
        personality="Amistosa y curiosa",
        sex=Sex.female,
        birth_date=datetime(2011, 10, 10),
        entry_date=datetime(2022, 10, 9),
        is_castrated=True,
        is_animal_compatible=True,
        image="https://cdn2.thecatapi.com/images/9vh.jpg",
        yard=yards[0],
        treatments=[
            Treatment(
                name="Cicaplast",
                zone="Lomo",
                frequency=1440,
                end_date=datetime(2024, 10, 17, 18, 30),
                amount="12 ml",
            ),
            Treatment(
                name="Malta",
                frequency=360,
            ),
            Treatment(
                name="Jarabe",
                frequency=17280,
            ),
            Treatment(
                name="Ibuprofeno",
                frequency=720,
                end_date=datetime(2024, 9, 30, 10, 0),
                amount="400 mg",
            ),
            Treatment(
                name="Pastilla desparasitación",
                frequency=2880,
                end_date=datetime(2024, 11, 15, 15, 45),
                amount="500 mg",
            ),
            Treatment(
                name="Paracetamol",
                frequency=1440,
            ),
        ],
        appointments=[
            Appointment(
                date=datetime(2024, 10, 17, 18, 30), description="Vacuna calcivirus para gato"
            ),
            Appointment(date=datetime(2024, 7, 5, 15, 0), description="Chequeo médico anual"),
            Appointment(date=datetime(2024, 8, 12, 10, 15), description="Revisión odontológica"),
            Appointment(date=datetime(2024, 6, 3, 9, 0), description="Consulta de dermatología"),
            Appointment(
                date=datetime(2024, 11, 8, 11, 0), description="Vacuna parvovirus para cachorro"
            ),
            Appointment(date=datetime(2024, 12, 15, 16, 45), description="Cirugía programada"),
            Appointment(date=datetime(2024, 7, 22, 17, 30), description="Control de peso y dieta"),
            Appointment(
                date=datetime(2024, 5, 17, 18, 30), description="Vacuna contra la leptospirosis"
            ),
        ],
    ),
    Animal(
        name="Tiger",
        description="Tiger es un gato aventurero y valiente. Le encanta explorar los alrededores y nunca dice que no a una nueva aventura. Su coraje y espíritu intrépido lo hacen destacar entre los demás.",
        personality="Aventurero y valiente",
        sex=Sex.male,
        birth_date=datetime(2020, 7, 3),
        entry_date=datetime(2023, 3, 22),
        is_castrated=False,
        is_animal_compatible=False,
        image="https://cdn2.thecatapi.com/images/27r.jpg",
        yard=yards[0],
    ),
    Animal(
        name="Simón",
        description="Simón es un gato juguetón y enérgico. Le encanta correr por toda la casa persiguiendo juguetes y explorando cada rincón. Siempre está listo para una sesión de juego con su familia humana.",
        personality="Juguetón y enérgico",
        sex=Sex.male,
        birth_date=datetime(2019, 5, 15),
        entry_date=datetime(2022, 12, 20),
        is_castrated=False,
        is_animal_compatible=True,
        image="https://cdn2.thecatapi.com/images/abc.jpg",
        yard=yards[1],
        treatments=[
            Treatment(
                name="Paracetamol",
                frequency=720,
            )
        ],
    ),
    Animal(
        name="Lola",
        description="Lola es una gatita traviesa y juguetona. Siempre está buscando nuevas formas de divertirse y mantener entretenida a su familia humana. Su energía contagiosa ilumina cualquier habitación.",
        personality="Traviesa y juguetona",
        sex=Sex.female,
        birth_date=datetime(2021, 1, 8),
        entry_date=datetime(2023, 11, 11),
        is_castrated=True,
        is_animal_compatible=False,
        appointments=[
            Appointment(date=datetime(2024, 7, 17, 18, 00), description="Revisión patita")
        ],
        yard=yards[2],
    ),
    Animal(
        name="Bolita",
        description="Bolita es una gatita traviesa y juguetona. Siempre está buscando nuevas formas de divertirse y mantener entretenida a su familia humana. Su energía contagiosa ilumina cualquier habitación.",
        personality="Traviesa y juguetona",
        sex=Sex.female,
        birth_date=datetime(2021, 1, 8),
        entry_date=datetime(2023, 11, 11),
        is_castrated=True,
        is_animal_compatible=False,
        appointments=[
            Appointment(date=datetime(2024, 7, 2, 18, 00), description="Revisión patita")
        ],
        yard=yards[2],
    ),
]


async def init_database_data():
    try:
        sql_session_generator = get_sql_session()
        sql_session = next(sql_session_generator)

        list(map(sql_session.add, animals))
        list(map(sql_session.add, people))

        sql_session.commit()

        list(map(sql_session.refresh, animals))
        list(map(sql_session.refresh, people))

        informs = [
            Inform.model_validate(
                dict(
                    creator=dict(people[0]),
                    volunteers=[dict(people[1])],
                    start_time=datetime(2024, 7, 15, 16, 30),
                    end_time=datetime(2024, 7, 15, 20, 0),
                    highlights=["Todo estaba muy ordenado"],
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[0].yard)),
                            animal=dict(animals[0]),
                            text="Estaba perfecta",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[1].yard)),
                            animal=dict(animals[1]),
                            text="Hoy ha sido probado con perros",
                        ),
                    ],
                    arrivals=[dict(name="Lulu", description="Gata blanca con manchas marrones")],
                    tested_animals=[
                        dict(
                            animal=dict(animals[1]),
                            compatible=False,
                        )
                    ],
                )
            ),
            Inform.model_validate(
                dict(
                    creator=dict(people[1]),
                    volunteers=[dict(people[0])],
                    start_time=datetime(2024, 7, 16, 16, 30),
                    end_time=datetime(2024, 7, 16, 20, 0),
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[2].yard)),
                            animal=dict(animals[2]),
                            text="Tenía un comportamiento normal",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[0].yard)),
                            animal=dict(animals[0]),
                            text="Se encontraba regular",
                        ),
                    ],
                    tested_animals=[
                        dict(
                            animal=dict(animals[2]),
                            compatible=True,
                        )
                    ],
                    adoptions=[
                        dict(
                            animal=dict(animals[3]),
                            foster=False,
                        )
                    ],
                    losses=[dict(animal=dict(animals[4]))],
                )
            ),
        ]

        await Inform.insert_many(informs)

        next(sql_session_generator)
    except StopIteration:
        print("Data initialization is finished!")
