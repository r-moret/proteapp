from proteapp.api.deps import get_session
from proteapp.models.animals import Animal, Sex
from datetime import datetime

from proteapp.models.treatments import Treatment

animals = [
    Animal(
        name="Carolina",
        yard="Patio 1",
        description="Carolina es una hermosa gata con un pelaje suave y lujoso. Disfruta tomando el sol y acurrucándose con sus compañeros humanos. A pesar de su apariencia regia, Carolina es increíblemente amigable y le encanta conocer gente nueva y otros animales.",
        personality="Amistosa y curiosa",
        sex=Sex.female,
        birth_date=datetime(2011, 10, 10),
        entry_date=datetime(2022, 10, 9),
        is_castrated=True,
        is_animal_compatible=True,
        image="https://cdn2.thecatapi.com/images/9vh.jpg",
        treatments=[
            Treatment(
                name="Cicaplast",
                zone="Lomo",
                frequency=1440,
            ),
            Treatment(
                name="Malta",
                frequency=360,
            ),
        ],
    ),
    Animal(
        name="Tiger",
        yard="Patio 1",
        description="Tiger es un gato aventurero y valiente. Le encanta explorar los alrededores y nunca dice que no a una nueva aventura. Su coraje y espíritu intrépido lo hacen destacar entre los demás.",
        personality="Aventurero y valiente",
        sex=Sex.male,
        birth_date=datetime(2020, 7, 3),
        entry_date=datetime(2023, 3, 22),
        is_castrated=False,
        is_animal_compatible=False,
        image="https://cdn2.thecatapi.com/images/27r.jpg",
    ),
    Animal(
        name="Simón",
        yard="Patio 2",
        description="Simón es un gato juguetón y enérgico. Le encanta correr por toda la casa persiguiendo juguetes y explorando cada rincón. Siempre está listo para una sesión de juego con su familia humana.",
        personality="Juguetón y enérgico",
        sex=Sex.male,
        birth_date=datetime(2019, 5, 15),
        entry_date=datetime(2022, 12, 20),
        is_castrated=False,
        is_animal_compatible=True,
        image="https://cdn2.thecatapi.com/images/abc.jpg",
        treatments=[
            Treatment(
                name="Paracetamol",
                frequency=720,
            )
        ],
    ),
    Animal(
        name="Lola",
        yard="Patio inmunodeficiencia",
        description="Lola es una gatita traviesa y juguetona. Siempre está buscando nuevas formas de divertirse y mantener entretenida a su familia humana. Su energía contagiosa ilumina cualquier habitación.",
        personality="Traviesa y juguetona",
        sex=Sex.female,
        birth_date=datetime(2021, 1, 8),
        entry_date=datetime(2023, 11, 11),
        is_castrated=True,
        is_animal_compatible=False,
    ),
]


def init_database_data():
    try:
        session_generator = get_session()
        session = next(session_generator)

        list(map(session.add, animals))

        session.commit()

        next(session_generator)
    except StopIteration:
        print("Initialization FINISHED!")
