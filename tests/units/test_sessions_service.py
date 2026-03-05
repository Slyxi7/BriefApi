import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.models.base import Base
from app.models.session import Session as SessionModel
from app.services.sessions_service import SessionService


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_get_all_sessions_service(db_session):

    session1 = SessionModel(
        formation_id=1,
        date_debut=datetime(2025, 1, 1),
        date_fin=datetime(2025, 1, 10),
        capacite=10
    )

    session2 = SessionModel(
        formation_id=1,
        date_debut=datetime(2025, 2, 1),
        date_fin=datetime(2025, 2, 10),
        capacite=15
    )

    db_session.add(session1)
    db_session.add(session2)
    db_session.commit()

    result = SessionService.get_all_sessions(db_session)

    assert len(result) == 2
    assert result[0].capacite == 10
    assert result[1].capacite == 15