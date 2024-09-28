from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, Page
from proteapp.api.animals.schemas import CompleteAnimal
from itertools import groupby
from typing import Any
from ulid import ULID

env = Environment(loader=FileSystemLoader(searchpath="proteapp/templates"))


def humanize_frequency(minutes: int | None):
    if minutes is None:
        return None

    if (weeks := (minutes / 10080)).is_integer():
        return f"cada {int(weeks)} semanas" if weeks > 1 else "cada semana"
    elif (days := (minutes / 1440)).is_integer():
        return f"cada {int(days)} días" if days > 1 else "cada día"
    elif (hours := (minutes / 60)).is_integer():
        return f"cada {int(hours)} horas" if hours > 1 else "cada hora"
    else:
        hours = minutes // 60
        rest = minutes % 60
        return f"cada {int(hours)} hora{'s' if hours > 1 else ''} y {int(rest)} minuto{'s' if rest > 1 else ''}"


def display_treatment(treatment: CompleteAnimal.Treatment) -> str:
    first_line = " - ".join(
        [info for info in [treatment.name, treatment.zone, treatment.amount] if info]
    )

    second_line = (
        f"({humanize_frequency(treatment.frequency)}"
        + (f", hasta el {treatment.end_date.strftime('%d de %b.')}" if treatment.end_date else "")
        + ")"
    )

    return first_line + "<br>" + second_line


def create_report(animals: list[CompleteAnimal], output_filename: str):
    template = env.get_template("report.html")

    no_yard_ulid = ULID()

    processed_animals: list[dict[str, Any]] = [
        {
            **animal.model_dump(),
            "sex": "Macho" if animal.sex == "male" else "Hembra",
            "treatments": [display_treatment(treatment) for treatment in animal.treatments],
            "yard": (
                dict(animal.yard)
                if animal.yard
                else dict(CompleteAnimal.Yard(id=no_yard_ulid, name="Sin patio"))
            ),
        }
        for animal in animals
    ]

    animals_by_yard = groupby(
        sorted(processed_animals, key=lambda x: x["yard"]["id"]),
        key=lambda x: x["yard"],
    )

    doc = None
    pages: list[dict[str, str | list[Page]]] = []

    for yard, yard_animals in animals_by_yard:
        html = template.render(animals=yard_animals, yard=yard["name"])
        doc = HTML(string=html).render()

        pages.append({"yard": yard["name"], "pages": doc.pages})

    sorted_pages = [
        page
        for yard_pages in sorted(pages, key=lambda x: x["yard"])
        for page in yard_pages["pages"]
    ]

    if doc is None:
        raise ValueError("There is no pages to create the report PDF")

    doc.copy(sorted_pages).write_pdf(output_filename)  # type: ignore
