import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from repositories.event_repository import EventRepository
from models import Event
from schemas import EventSchema, EventRequest

@pytest.fixture
def event_instance():
    # Create an example event instance for testing
    event = EventSchema(
        name="Test Event",
        created_date=datetime.utcnow(),
        application_id=1,
        organization_id=1
    )
    return event

def test_create_event(session: Session, event_instance: EventSchema):
    # Instantiate the repository
    event_repository = EventRepository(session)

    # Call the create_event function
    created_event = event_repository.create_event(session, event_instance)

    # Verify that the event was saved to the database
    event_db = session.query(Event).filter_by(id=created_event.id).one_or_none()
    assert event_db is not None
    assert event_db.name == event_instance.name
    assert event_db.created_date == event_instance.created_date
    assert event_db.application_id == event_instance.application_id
    assert event_db.organization_id == event_instance.organization_id
