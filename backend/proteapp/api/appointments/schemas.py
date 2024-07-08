from proteapp.models.appointments import BaseAppointment


class CreateAppointment(BaseAppointment): ...


class PublicAppointment(BaseAppointment):
    id: int
