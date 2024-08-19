from proteapp.api.monitorings.schemas import EditableMonitoring
from proteapp.models.sql.monitorings import Monitoring
from proteapp.models.sql.adoptions import Adoption
from proteapp.api.deps import sql_engine
from sqlmodel import Session
from datetime import datetime
from proteapp.exceptions import UnsavedDataError


def to_monitoring(data: EditableMonitoring) -> Monitoring:
    with Session(sql_engine) as session:
        monitoring_adoption = session.get(Adoption, data.adoption)

        if not monitoring_adoption:
            raise UnsavedDataError(
                "Cannot create an monitoring with an adoption that doesn't exist",
                field="adoption",
            )
        valid_date = data.follow_date
        if isinstance(valid_date, datetime):
            valid_date = valid_date.date()

        return Monitoring.model_validate(
            {**dict(data), "adoption_id": monitoring_adoption.id, "follow_date": valid_date}
        )
