from zoneinfo import ZoneInfo
from proteapp.api.deps import get_sql_session
from datetime import datetime, date, time
from typing import cast
from ulid import ULID

from proteapp.models.sql.animals import Animal, Sex
from proteapp.models.sql.treatments import Treatment
from proteapp.models.sql.appointments import Appointment
from proteapp.models.sql.yards import Yard
from proteapp.models.nosql.yard_order import YardOrder
from proteapp.models.sql.users import User, Role
from proteapp.models.sql.people import Person
from proteapp.models.sql.adoptions import Adoption
from proteapp.models.sql.monitorings import Monitoring
from proteapp.models.nosql.inform import Inform
from proteapp.models.nosql.shift import Shift

people = [
    Person(
        name="Cris",
        first_surname="Espejo",
        phone="640040545",
        email="cristinaespejo@gmail.com",
        user=User(
            id=ULID.from_str("01J3DSAAMJCCXJNB7M2XZGVEPW"),  # Fixed, this is the fake logged user
            active=True,
            veteran=False,
            hashed_password="$2b$12$uGvFa6aQ5V/ciqbWwvRWkuL5fpPowr2.iW1FA0tSKGG2L0XmdEpEC",
            role=Role.admin,
        ),
    ),
    Person(
        name="Rafael",
        first_surname="Moret",
        phone="640564432",
        email="rafaelmoret@gmail.com",
        user=User(
            image="images/01J8N4H0J20BTE53ZH65AXFGMX.jpg",
            active=True,
            veteran=True,
            hashed_password="$2b$12$S098AHvdtzW1Tmh0t/PrWumjMCw0aRSutfVV4CVMB/o69jC2ufDSC",
        ),
    ),
    Person(
        name="Ana",
        first_surname="García",
        second_surname="Sánchez",
        phone="612345678",
        email="anagarcia@example.com",
        user=User(
            image="images/01J8N4GTKRSQPWVBQ0DV61D4BJ.jpg",
            active=True,
            veteran=True,
            hashed_password="$2b$12$K6gDRE0yQ7bQwHJvMHc6N.8tTtfgEBPI30TtKzT4cWmQZf5oMEloy",
            role=Role.admin,
        ),
    ),
    Person(
        name="Luis",
        first_surname="Pérez",
        phone="623456789",
        email="luisperez@example.com",
    ),
    Person(
        name="Marta",
        first_surname="López",
        phone="634567890",
        email="martalopez@example.com",
        user=User(
            image="images/01J8N4H668MYTTMXN2DNTKZTDY.jpg",
            active=True,
            veteran=False,
            hashed_password="$2b$12$F5K2WvLg6e9OeOITddwnLuEPH1c/keM.k7FjY7bUqgr0b72ThxW5.",
            role=Role.admin,
        ),
    ),
    Person(
        name="Javier",
        first_surname="Martín",
        second_surname="Torres",
        phone="645678901",
        email="javiermartin@example.com",
    ),
    Person(
        name="Sofía",
        first_surname="Fernández",
        phone="656789012",
        email="sofiafernandez@example.com",
        user=User(
            image="images/01J8N4GWHS9MNH0E177Q3QY4TE.jpg",
            active=True,
            veteran=True,
            hashed_password="$2b$12$A0F1W4T2V2eQnMxvVcloJuRQ4AW2WZ2.dpbk4a4QPUhW3BZPZ4RhG",
        ),
    ),
    Person(
        name="Diego",
        first_surname="Hernández",
        phone="667890123",
        email="diegohernandez@example.com",
    ),
    Person(
        name="Carla",
        first_surname="Jiménez",
        phone="678901234",
        email="carlajimenez@example.com",
    ),
    Person(
        name="Roberto",
        first_surname="Gómez",
        phone="689012345",
        email="robertogomez@example.com",
    ),
    Person(
        name="Elena",
        first_surname="Morales",
        second_surname="Díaz",
        phone="690123456",
        email="elenamorales@example.com",
    ),
    Person(
        name="Samuel",
        first_surname="Vázquez",
        phone="691234567",
        email="samuelvazquez@example.com",
        user=User(
            image="images/01J8N4GXGV1G6Q6JF1RKGCYMD2.jpg",
            active=True,
            veteran=False,
            hashed_password="$2b$12$H7U3j2kqU6FSxPqHeQyZZ.dCFfYy5X2r2i3x6P/ZZ1ZHvDq8dI8de",
        ),
    ),
    Person(
        name="Lucía",
        first_surname="Ríos",
        second_surname="Cruz",
        phone="692345678",
        email="luciarios@example.com",
        user=User(
            image="images/01J8N4GVJJB18Q213JXBWJ944J.jpg",
            active=True,
            veteran=True,
            hashed_password="$2b$12$L8j1fI4m0EkhKUkxL.vG8e/.5kExyUk5tEVPbPS9DaX1Hi11hs4pO",
            role=Role.admin,
        ),
    ),
    Person(
        name="Fernando",
        first_surname="Salas",
        phone="693456789",
        email="fernandosalas@example.com",
    ),
    Person(
        name="Teresa",
        first_surname="Cordero",
        phone="694567890",
        email="teresacordero@example.com",
    ),
    Person(
        name="Pablo",
        first_surname="Moreno",
        second_surname="Guerrero",
        phone="695678901",
        email="pablomoreno@example.com",
    ),
]

yards = [
    Yard(name="Patio 1"),
    Yard(name="Patio 2"),
    Yard(name="Patio 3"),
    Yard(name="Patio 4"),
    Yard(name="Patio 5"),
    Yard(name="Patio inmunodeficiencia"),
    Yard(name="Patio calcivirus"),
]


animals = [
    Animal(
        name="Obi",
        description="Obi es un hermoso gato con un pelaje suave y lujoso. Disfruta tomando el sol y acurrucándose con sus compañeros humanos. A pesar de su apariencia regia, Obi es increíblemente amigable y le encanta conocer gente nueva y otros animales.",
        personality="Amistoso y curioso",
        sex=Sex.male,
        birth_date=datetime(2011, 10, 10),
        entry_date=datetime(2022, 10, 9),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N2PGWJ5F1A5K37DHCWWP3K.jpg",
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
        name="Milo",
        description="Milo es un gato curioso con un pelaje atigrado. Le encanta trepar y pasar tiempo explorando su entorno. Siempre está atento a cualquier movimiento y le encanta cazar juguetes.",
        personality="Curioso y aventurero",
        sex=Sex.male,
        birth_date=datetime(2019, 8, 21),
        entry_date=datetime(2023, 5, 30),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0V7ZXZEJ20JTZDPEDN4MX.jpg",
        treatments=[
            Treatment(
                name="Antipulgas",
                zone="Cuello",
                frequency=1440,
                end_date=datetime(2024, 11, 10, 9, 0),
                amount="10 ml",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 17, 10, 0), description="Chequeo anual"),
        ],
    ),
    Animal(
        name="Toby",
        description="Toby es un gato grande y tranquilo con un pelaje suave. Disfruta de las largas siestas y es muy cariñoso con las personas de confianza.",
        personality="Relajado y afectuoso",
        sex=Sex.male,
        birth_date=datetime(2016, 12, 14),
        entry_date=datetime(2023, 7, 15),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0V855VHX1D4EQM6GVJ4Q0.jpg",
        treatments=[
            Treatment(
                name="Desparasitante",
                frequency=2880,
                end_date=datetime(2024, 12, 5, 15, 0),
                amount="400 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 9, 5, 11, 0), description="Consulta veterinaria"),
        ],
    ),
    Animal(
        name="Bella",
        description="Bella es una gata juguetona con un pelaje blanco y manchas negras. Es muy activa y le encanta interactuar con otros gatos y con las personas.",
        personality="Juguetona y social",
        sex=Sex.female,
        birth_date=datetime(2020, 3, 11),
        entry_date=datetime(2023, 8, 1),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0V8V6P21DEDMEEPEXWFXC.jpg",
        treatments=[
            Treatment(
                name="Ibuprofeno",
                frequency=720,
                end_date=datetime(2024, 9, 30, 12, 0),
                amount="400 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 12, 9, 0), description="Revisión general"),
        ],
    ),
    Animal(
        name="Sombra",
        description="Sombra es un gato de pelaje oscuro y ojos brillantes. Es muy independiente, pero siempre vuelve a buscar caricias cuando está de humor.",
        personality="Independiente y misterioso",
        sex=Sex.male,
        birth_date=datetime(2017, 7, 29),
        entry_date=datetime(2023, 9, 22),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0V9GXRPYK6BT2H9QHZCKC.jpg",
        treatments=[
            Treatment(
                name="Advocate",
                zone="Lomo",
                frequency=1440,
                end_date=datetime(2024, 10, 18, 14, 0),
                amount="12 ml",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 5, 10, 0), description="Vacunación anual"),
        ],
    ),
    Animal(
        name="Mina",
        description="Mina es una gata pequeña y ágil. Tiene un pelaje gris oscuro y le encanta jugar con cuerdas y pequeños objetos.",
        personality="Ágil y curiosa",
        sex=Sex.female,
        birth_date=datetime(2019, 10, 17),
        entry_date=datetime(2023, 10, 3),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0VA7CKAN2V2J0R86ZAQJC.jpg",
        yard=yards[0],
        treatments=[
            Treatment(
                name="Paracetamol",
                frequency=1440,
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 22, 11, 0), description="Revisión general"),
        ],
    ),
    Animal(
        name="Luna",
        description="Luna es una gata de pelaje gris claro con ojos brillantes. Es muy cariñosa y le encanta acurrucarse en lugares cálidos y tranquilos.",
        personality="Cariñosa y calmada",
        sex=Sex.female,
        birth_date=datetime(2018, 4, 5),
        entry_date=datetime(2023, 2, 10),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0VAW93EDHX5GCAHGR7511.jpg",
        yard=yards[3],
        treatments=[
            Treatment(
                name="Malta",
                frequency=720,
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 3, 12, 30), description="Chequeo general"),
        ],
    ),
    Animal(
        name="Gizmo",
        description="Gizmo es un gato de pelaje marrón y blanco con una actitud juguetona. Siempre está buscando algo para explorar y le encanta trepar por los muebles.",
        personality="Juguetón y curioso",
        sex=Sex.male,
        birth_date=datetime(2019, 2, 23),
        entry_date=datetime(2023, 6, 14),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0VBP2GSTM30ZESSFYZAHB.jpg",
        yard=yards[5],
        treatments=[
            Treatment(
                name="Antipulgas",
                zone="Dorso",
                frequency=1440,
                end_date=datetime(2024, 12, 1, 9, 0),
                amount="12 ml",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 25, 9, 0), description="Consulta veterinaria"),
        ],
    ),
    Animal(
        name="Salem",
        description="Salem es un gato negro con una mirada profunda. Es muy independiente, pero siempre regresa para recibir caricias y atención cuando lo desea.",
        personality="Independiente y misterioso",
        sex=Sex.male,
        birth_date=datetime(2016, 11, 10),
        entry_date=datetime(2023, 7, 2),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0VBTR21G1TQ3B5SJDAG66.jpg",
        yard=yards[6],
        treatments=[
            Treatment(
                name="Desparasitante",
                frequency=2880,
                end_date=datetime(2024, 10, 25, 10, 0),
                amount="500 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 9, 20, 12, 30), description="Vacunación anual"),
        ],
    ),
    Animal(
        name="Misha",
        description="Misha es una gata de pelaje blanco y ojos azules. Es muy juguetona y le encanta perseguir pelotas y otros juguetes por toda la casa.",
        personality="Juguetona y activa",
        sex=Sex.female,
        birth_date=datetime(2020, 5, 18),
        entry_date=datetime(2023, 8, 10),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0VCM0MJBJA1XWZA51S175.jpg",
        yard=yards[4],
        treatments=[
            Treatment(
                name="Ibuprofeno",
                frequency=720,
                end_date=datetime(2024, 10, 5, 15, 0),
                amount="200 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 15, 9, 0), description="Control de peso"),
        ],
    ),
    Animal(
        name="Felix",
        description="Felix es un gato de pelaje negro con manchas blancas. Es muy sociable y le encanta estar rodeado de gente. Siempre está buscando la atención de quienes lo cuidan.",
        personality="Sociable y amigable",
        sex=Sex.male,
        birth_date=datetime(2017, 3, 29),
        entry_date=datetime(2023, 9, 5),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0VD9JTRYYD4A5YFPR23XW.jpg",
        yard=yards[1],
        treatments=[
            Treatment(
                name="Paracetamol",
                frequency=1440,
            ),
        ],
        appointments=[
            Appointment(
                date=datetime(2024, 11, 30, 12, 30), description="Revisión médica general"
            ),
        ],
    ),
    Animal(
        name="Nina",
        description="Nina es una gata juguetona de pelaje blanco con rayas grises. Le encanta pasar tiempo explorando su entorno y jugando con otros gatos.",
        personality="Juguetona y sociable",
        sex=Sex.female,
        birth_date=datetime(2019, 6, 12),
        entry_date=datetime(2023, 4, 15),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WCWR730TTACERN8WYW9D.jpg",
        yard=yards[2],
        treatments=[
            Treatment(
                name="Malta",
                frequency=360,
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 9, 22, 15, 0), description="Chequeo médico"),
        ],
    ),
    Animal(
        name="Simba",
        description="Simba es un gato ágil y enérgico. Tiene un pelaje dorado con manchas blancas. Siempre está en movimiento y es muy curioso.",
        personality="Enérgico y curioso",
        sex=Sex.male,
        birth_date=datetime(2018, 8, 17),
        entry_date=datetime(2023, 6, 22),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WDRMM9S7C1TC6J52AFT9.jpg",
        yard=yards[0],
        treatments=[
            Treatment(
                name="Advocate",
                zone="Cuello",
                frequency=1440,
                end_date=datetime(2024, 12, 20, 11, 0),
                amount="10 ml",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 30, 10, 0), description="Revisión general"),
        ],
    ),
    Animal(
        name="Lola",
        description="Lola es una gata tranquila y cariñosa. Disfruta de largas siestas y es muy apegada a su dueño. Tiene un pelaje blanco con manchas negras.",
        personality="Calmada y cariñosa",
        sex=Sex.female,
        birth_date=datetime(2017, 3, 14),
        entry_date=datetime(2023, 7, 3),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WENZS4NXJ1X54WA4DXN2.jpg",
        yard=yards[4],
        treatments=[
            Treatment(
                name="Ibuprofeno",
                frequency=720,
                end_date=datetime(2024, 11, 10, 14, 0),
                amount="400 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 9, 14, 12, 0), description="Vacunación"),
        ],
    ),
    Animal(
        name="Max",
        description="Max es un gato activo y siempre está explorando. Tiene un pelaje atigrado y ojos verdes brillantes. Le encanta jugar con cualquier objeto que encuentre.",
        personality="Activo y curioso",
        sex=Sex.male,
        birth_date=datetime(2020, 1, 25),
        entry_date=datetime(2023, 8, 16),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WFA6TCE2D48MN7DG9JS4.jpg",
        yard=yards[3],
        treatments=[
            Treatment(
                name="Desparasitante",
                frequency=2880,
                end_date=datetime(2024, 12, 1, 9, 0),
                amount="500 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 18, 11, 0), description="Consulta veterinaria"),
        ],
    ),
    Animal(
        name="Cleo",
        description="Cleo es una gata elegante con un pelaje negro y suave. Es muy cariñosa y le encanta estar cerca de las personas, siempre buscando atención y mimos.",
        personality="Cariñosa y leal",
        sex=Sex.female,
        birth_date=datetime(2016, 9, 9),
        entry_date=datetime(2023, 9, 29),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N2YGCJF0P9HV0B91928266.jpg",
        yard=yards[1],
        treatments=[
            Treatment(
                name="Paracetamol",
                frequency=1440,
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 19, 9, 30), description="Revisión médica"),
        ],
    ),
    Animal(
        name="Toby",
        description="Toby es un gato de pelaje atigrado con un carácter juguetón. Siempre está dispuesto a jugar y explorar su entorno, lo que lo hace muy entretenido.",
        personality="Juguetón y curioso",
        sex=Sex.male,
        birth_date=datetime(2021, 5, 22),
        entry_date=datetime(2023, 3, 15),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WGTT6YAAERHZC0YS1XF9.jpg",
        yard=yards[5],
        treatments=[
            Treatment(
                name="Malta",
                frequency=360,
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 9, 25, 14, 0), description="Chequeo veterinario"),
        ],
    ),
    Animal(
        name="Chester",
        description="Chester es un gato robusto con un pelaje gris oscuro. Es muy tranquilo y disfruta de pasar tiempo en el regazo de su dueño.",
        personality="Tranquilo y cariñoso",
        sex=Sex.male,
        birth_date=datetime(2018, 12, 3),
        entry_date=datetime(2023, 8, 21),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WHGAF6VQ2NH5JT6DREY9.jpg",
        yard=yards[2],
        treatments=[
            Treatment(
                name="Cicaplast",
                zone="Patas",
                frequency=1440,
                end_date=datetime(2024, 10, 10, 10, 0),
                amount="10 ml",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 15, 11, 0), description="Vacunación anual"),
        ],
    ),
    Animal(
        name="Milo",
        description="Milo es un gato de pelaje marrón claro con ojos ávidos. Es muy curioso y siempre está explorando cada rincón de la casa.",
        personality="Curioso y aventurero",
        sex=Sex.male,
        birth_date=datetime(2020, 4, 15),
        entry_date=datetime(2023, 7, 11),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WHMP52T6ZVKBVZAABHEX.jpg",
        yard=yards[0],
        treatments=[
            Treatment(
                name="Desparasitante",
                frequency=2880,
                end_date=datetime(2024, 12, 1, 9, 0),
                amount="500 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 10, 12, 0), description="Control de salud"),
        ],
    ),
    Animal(
        name="Zara",
        description="Zara es una gata elegante de pelaje negro con manchas blancas. Es muy afectuosa y le encanta estar rodeada de personas.",
        personality="Amigable y cariñosa",
        sex=Sex.female,
        birth_date=datetime(2019, 1, 30),
        entry_date=datetime(2023, 6, 5),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WHRX2JJAVJQ6NFPH66SZ.jpg",
        yard=yards[3],
        treatments=[
            Treatment(
                name="Ibuprofeno",
                frequency=720,
                end_date=datetime(2024, 10, 5, 14, 0),
                amount="200 mg",
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 11, 5, 10, 30), description="Vacunación"),
        ],
    ),
    Animal(
        name="Coco",
        description="Coco es un gato de pelaje gris oscuro y ojos amarillos. Es muy independiente y disfruta de pasar tiempo a solas, aunque también aprecia los mimos.",
        personality="Independiente y cariñoso",
        sex=Sex.male,
        birth_date=datetime(2016, 7, 14),
        entry_date=datetime(2023, 5, 28),
        is_castrated=True,
        is_animal_compatible=True,
        image="images/01J8N0WJPN52281QGR4SCHZX5E.jpg",
        yard=yards[1],
        treatments=[
            Treatment(
                name="Malta",
                frequency=360,
            ),
        ],
        appointments=[
            Appointment(date=datetime(2024, 10, 20, 9, 0), description="Chequeo veterinario"),
        ],
    ),
]

adoptions = [
    Adoption(
        animal=animals[2],
        person=people[5],
        foster=False,
        register_date=date(2024, 2, 15),
        monitorings=[
            Monitoring(
                follow_date=date(2021, 8, 3),
                note="Ha pasado una buena noche y es muy cariñoso con el resto",
            ),
            Monitoring(
                follow_date=date(2021, 11, 5),
                note="Ha tenido que ir al veterinario por un problema con la pata",
            ),
            Monitoring(
                follow_date=date(2021, 12, 5),
                note="Se ha adaptado correctamente, se cierra el seguimiento",
            ),
        ],
    ),
    Adoption(
        animal=animals[3],
        person=people[7],
        foster=False,
        register_date=date(2021, 1, 8),
    ),
    Adoption(
        animal=animals[1],
        person=people[3],
        foster=True,
        register_date=date(2019, 9, 24),
        monitorings=[
            Monitoring(
                follow_date=date(2019, 10, 4),
                note="Le ha costado ir al arenero desde que está en casa",
            ),
            Monitoring(
                follow_date=date(2020, 11, 4),
                note="Se lleva estupendamente con el otro gato de la familia",
            ),
        ],
    ),
    Adoption(
        animal=animals[4],
        person=people[8],
        foster=True,
        register_date=date(2023, 5, 2),
    ),
]


async def init_database_data():
    try:
        sql_session_generator = get_sql_session()
        sql_session = next(sql_session_generator)

        list(map(sql_session.add, animals))
        list(map(sql_session.add, people))
        list(map(sql_session.add, adoptions))

        sql_session.commit()

        list(map(sql_session.refresh, animals))
        list(map(sql_session.refresh, people))

        yards_order = [
            YardOrder.model_validate(
                dict(
                    date=datetime(2024, 7, 20),
                    yard_order=[
                        dict(id=yards[0].id, name=yards[0].name),
                        dict(id=yards[1].id, name=yards[1].name),
                        dict(id=yards[2].id, name=yards[2].name),
                    ],
                )
            ),
            YardOrder.model_validate(
                dict(
                    date=datetime(2024, 8, 20),
                    yard_order=[
                        dict(id=yards[1].id, name=yards[1].name),
                        dict(id=yards[0].id, name=yards[0].name),
                        dict(id=yards[3].id, name=yards[3].name),
                        dict(id=yards[2].id, name=yards[2].name),
                        dict(id=yards[4].id, name=yards[4].name),
                        dict(id=yards[6].id, name=yards[6].name),
                        dict(id=yards[5].id, name=yards[5].name),
                    ],
                )
            ),
        ]

        informs = [
            Inform.model_validate(
                dict(
                    creator=dict(cast(User, people[0].user)) | dict(person=dict(people[0])),
                    volunteers=[dict(cast(User, people[1].user)) | dict(person=dict(people[1]))],
                    date=date(2024, 7, 14),
                    time_range=dict(
                        start=time(10, 30, tzinfo=ZoneInfo("Europe/Madrid")),
                        end=time(13, 0, tzinfo=ZoneInfo("Europe/Madrid")),
                    ),
                    highlights=["Todo estaba muy ordenado"],
                    yard_order=[dict(yard) for yard in yards_order[-1].yard_order],
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[0].yard)),
                            animal=dict(animals[0]),
                            text="Estaba perfecta",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[5].yard)),
                            animal=dict(animals[5]),
                            text="Hoy ha sido probado con perros",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[13].yard)),
                            animal=dict(animals[13]),
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
                    creator=dict(cast(User, people[6].user)) | dict(person=dict(people[6])),
                    volunteers=[dict(cast(User, people[11].user)) | dict(person=dict(people[11]))],
                    date=date(2024, 7, 15),
                    time_range=dict(
                        start=time(16, 30, tzinfo=ZoneInfo("Europe/Madrid")),
                        end=time(20, 0, tzinfo=ZoneInfo("Europe/Madrid")),
                    ),
                    yard_order=[dict(yard) for yard in yards_order[-1].yard_order],
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[5].yard)),
                            animal=dict(animals[5]),
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
            Inform.model_validate(
                dict(
                    creator=dict(cast(User, people[2].user)) | dict(person=dict(people[2])),
                    volunteers=[dict(cast(User, people[4].user)) | dict(person=dict(people[4]))],
                    date=date(2024, 8, 15),
                    time_range=dict(
                        start=time(11, 0, tzinfo=ZoneInfo("Europe/Madrid")),
                        end=time(14, 30, tzinfo=ZoneInfo("Europe/Madrid")),
                    ),
                    highlights=["Hubo una limpieza profunda del área de juego"],
                    yard_order=[dict(yard) for yard in yards_order[-1].yard_order],
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[5].yard)),
                            animal=dict(animals[5]),
                            text="Ha mejorado su comportamiento con los cuidadores",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[7].yard)),
                            animal=dict(animals[7]),
                            text="Se le realizó un examen de salud rutinario",
                        ),
                    ],
                    arrivals=[dict(name="Bella", description="Perra mestiza muy sociable")],
                    tested_animals=[
                        dict(
                            animal=dict(animals[5]),
                            compatible=False,
                        )
                    ],
                )
            ),
            Inform.model_validate(
                dict(
                    creator=dict(cast(User, people[4].user)) | dict(person=dict(people[4])),
                    volunteers=[dict(cast(User, people[1].user)) | dict(person=dict(people[1]))],
                    date=date(2024, 9, 5),
                    time_range=dict(
                        start=time(10, 30, tzinfo=ZoneInfo("Europe/Madrid")),
                        end=time(13, 0, tzinfo=ZoneInfo("Europe/Madrid")),
                    ),
                    highlights=["El entrenamiento en obediencia básica fue un éxito"],
                    yard_order=[dict(yard) for yard in yards_order[-1].yard_order],
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[7].yard)),
                            animal=dict(animals[7]),
                            text="Respondió bien al entrenamiento, muy receptivo",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[8].yard)),
                            animal=dict(animals[8]),
                            text="Todavía tiene que trabajar en su socialización",
                        ),
                    ],
                    arrivals=[dict(name="Tom", description="Gato siamés de carácter tímido")],
                    tested_animals=[
                        dict(
                            animal=dict(animals[6]),
                            compatible=True,
                        )
                    ],
                )
            ),
            Inform.model_validate(
                dict(
                    creator=dict(cast(User, people[2].user)) | dict(person=dict(people[2])),
                    volunteers=[dict(cast(User, people[4].user)) | dict(person=dict(people[4]))],
                    date=date(2024, 9, 12),
                    time_range=dict(
                        start=time(8, 30, tzinfo=ZoneInfo("Europe/Madrid")),
                        end=time(11, 30, tzinfo=ZoneInfo("Europe/Madrid")),
                    ),
                    highlights=[
                        "Se incorporaron nuevas rutinas para mejorar el bienestar de los animales"
                    ],
                    yard_order=[dict(yard) for yard in yards_order[-1].yard_order],
                    notes=[
                        dict(
                            yard=dict(cast(Yard, animals[9].yard)),
                            animal=dict(animals[1]),
                            text="Mostró gran curiosidad por las nuevas actividades",
                        ),
                        dict(
                            yard=dict(cast(Yard, animals[12].yard)),
                            animal=dict(animals[3]),
                            text="Necesita más interacción con otros perros",
                        ),
                    ],
                    arrivals=[dict(name="Oscar", description="Conejo marrón muy curioso")],
                    tested_animals=[
                        dict(
                            animal=dict(animals[4]),
                            compatible=True,
                        )
                    ],
                )
            ),
        ]

        shift = Shift.model_validate(
            dict(
                status="open",
                timetable=dict(
                    monday=dict(
                        morning=[
                            cast(User, people[2].user).id,
                            cast(User, people[4].user).id,
                        ],
                        afternoon=[
                            cast(User, people[0].user).id,
                            cast(User, people[1].user).id,
                            cast(User, people[6].user).id,
                        ],
                    ),
                    thursday=dict(
                        morning=[cast(User, people[0].user).id],
                        afternoon=[
                            cast(User, people[1].user).id,
                            cast(User, people[2].user).id,
                        ],
                    ),
                    wednesday=dict(
                        morning=[
                            cast(User, people[0].user).id,
                            cast(User, people[6].user).id,
                            cast(User, people[2].user).id,
                        ],
                        afternoon=[],
                    ),
                    tuesday=dict(
                        morning=[
                            cast(User, people[0].user).id,
                            cast(User, people[1].user).id,
                        ],
                        afternoon=[
                            cast(User, people[4].user).id,
                        ],
                    ),
                    friday=dict(
                        morning=[],
                        afternoon=[
                            cast(User, people[4].user).id,
                            cast(User, people[6].user).id,
                        ],
                    ),
                    saturday=dict(
                        morning=[
                            cast(User, people[0].user).id,
                            cast(User, people[1].user).id,
                            cast(User, people[2].user).id,
                        ],
                        afternoon=[],
                    ),
                    sunday=dict(
                        morning=[],
                        afternoon=[],
                    ),
                ),
            )
        )

        await Inform.delete_all()
        await Inform.insert_many(informs)

        await Shift.delete_all()
        await Shift.insert_one(shift)

        await YardOrder.delete_all()
        await YardOrder.insert_many(yards_order)

        next(sql_session_generator)
    except StopIteration:
        print("Data initialization is finished!")
