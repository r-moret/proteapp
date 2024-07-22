from proteapp.api.appointments.schemas import EditableAppointment
from proteapp.models.sql.appointments import Appointment
from proteapp.models.sql.animals import Animal
from proteapp.api.deps import sql_engine
from sqlmodel import Session
from proteapp.exceptions import UnsavedDataError


def to_appointment(data: EditableAppointment) -> Appointment:
    with Session(sql_engine) as session:
        appointment_animal = session.get(Animal, data.animal)

        if not appointment_animal:
            raise UnsavedDataError(
                "Cannot create an appointment with an animal that doesn't exist",
                field="animal",
            )

        return Appointment.model_validate(
            {
                **dict(data),
                "animal_id": appointment_animal.id,
            }
        )
