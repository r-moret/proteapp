from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.deps import get_sql_session
from proteapp.api.appointments.schemas import EditableAppointment, CompleteAppointment
from proteapp.models.sql.appointments import Appointment
from sqlmodel import Session
from ulid import ULID
from proteapp.api.appointments.adapters import to_appointment
from proteapp.exceptions import UnsavedDataError
from pydantic import ValidationError

router = APIRouter(prefix="/appointment", tags=["appointment"])


@router.post("/", response_model=CompleteAppointment, status_code=201)
def post_appointment(
    appointment: EditableAppointment, session: Session = Depends(get_sql_session)
):
    try:
        appointment_db = to_appointment(appointment)
    except UnsavedDataError as e:
        raise HTTPException(
            422, f'The field "{e.field}" makes reference to an entity that is not saved yet'
        )
    except ValidationError:
        raise HTTPException(422, "Unable to create an appointment with the data passed")

    session.add(appointment_db)
    session.commit()
    session.refresh(appointment_db)

    return appointment_db


@router.delete("/{id}", status_code=204)
def delete_appointment(id: ULID, session: Session = Depends(get_sql_session)):
    appointment_db = session.get(Appointment, id)

    if appointment_db is None:
        raise HTTPException(404, "No animal found")

    session.delete(appointment_db)
    session.commit()
