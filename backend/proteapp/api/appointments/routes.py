from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.deps import get_sql_session
from proteapp.models.animals import Animal
from proteapp.api.appointments.schemas import CreateAppointment, PublicAppointment
from proteapp.models.appointments import Appointment
from sqlmodel import Session, select

router = APIRouter(prefix="/appointment", tags=["appointment"])


@router.get("/search", response_model=list[PublicAppointment])
def get_appointments(session: Session = Depends(get_sql_session)):
    return session.exec(select(Appointment)).all()


@router.post("/", response_model=PublicAppointment, status_code=201)
def post_appointment(appointment: CreateAppointment, session: Session = Depends(get_sql_session)):
    appointment_db = Appointment.model_validate(appointment)

    animal_db = session.get(Animal, appointment.animal_id)

    if not animal_db:
        raise HTTPException(404, "No animal found")

    animal_db.appointments.append(appointment_db)

    session.add(animal_db)
    session.commit()
    session.refresh(appointment_db)

    return appointment_db


@router.delete("/{id}")
def delete_appointment(id: int, session: Session = Depends(get_sql_session)):
    appointment_db = session.get(Appointment, id)

    if appointment_db is None:
        raise HTTPException(404, "No animal found")

    session.delete(appointment_db)
    session.commit()
