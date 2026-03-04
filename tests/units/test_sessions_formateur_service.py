import pytest
from unittest.mock import MagicMock, patch
from app.services.sessions_formateurs_service import SessionsFormateursService


def make_db():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.query.return_value.all.return_value = []
    return db

def make_sf(session_id=1, formateur_id=10):
    sf = MagicMock()
    sf.session_id = session_id
    sf.formateur_id = formateur_id
    return sf

def make_formateur(id=10, role="formateur"):
    u = MagicMock()
    u.id = id
    u.role = role
    return u

def make_data(session_id=1, formateur_id=10):
    d = MagicMock()
    d.session_id = session_id
    d.formateur_id = formateur_id
    return d

def test_get_all_returns_list():
    db = make_db()
    sfs = [make_sf(), make_sf(session_id=2)]
    db.query.return_value.all.return_value = sfs
    assert SessionsFormateursService.get_all(db) == sfs

def test_get_found():
    db = make_db()
    sf = make_sf()
    db.query.return_value.filter.return_value.first.return_value = sf
    assert SessionsFormateursService.get(db, 1, 10) is sf

def test_get_not_found():
    db = make_db()
    assert SessionsFormateursService.get(db, 1, 10) is None

def _db_for_create(session_exists=True, formateur_exists=True, formateur_role="formateur"):
    db = MagicMock()
    session_obj = MagicMock() if session_exists else None
    formateur_obj = make_formateur(role=formateur_role) if formateur_exists else None
    db.query.return_value.filter.return_value.first.side_effect = [session_obj, formateur_obj]
    return db

def test_create_raises_if_session_not_found():
    db = _db_for_create(session_exists=False)
    with pytest.raises(ValueError, match="session"):
        SessionsFormateursService.create(db, make_data())

def test_create_raises_if_formateur_not_found():
    db = _db_for_create(formateur_exists=False)
    with pytest.raises(ValueError, match="formateur"):
        SessionsFormateursService.create(db, make_data())

def test_create_raises_if_user_not_formateur():
    db = _db_for_create(formateur_role="stagiaire")
    with pytest.raises(ValueError, match="formateurs"):
        SessionsFormateursService.create(db, make_data())

def test_create_raises_if_already_assigned():
    db = _db_for_create()
    with patch.object(SessionsFormateursService, "get", return_value=make_sf()):
        with pytest.raises(ValueError, match="déjà affecté"):
            SessionsFormateursService.create(db, make_data())

def test_create_success():
    db = _db_for_create()
    with patch.object(SessionsFormateursService, "get", return_value=None):
        SessionsFormateursService.create(db, make_data())
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_update_returns_none_if_not_found():
    db = make_db()
    with patch.object(SessionsFormateursService, "get", return_value=None):
        assert SessionsFormateursService.update(db, 1, 10, MagicMock()) is None

def test_update_raises_if_new_session_not_found():
    db = make_db()
    sf = make_sf()
    data = MagicMock()
    data.model_dump.return_value = {"session_id": 99, "formateur_id": 10}
    db.query.return_value.filter.return_value.first.return_value = None

    with patch.object(SessionsFormateursService, "get", return_value=sf):
        with pytest.raises(ValueError, match="session"):
            SessionsFormateursService.update(db, 1, 10, data)

def test_update_raises_if_formateur_not_formateur_role():
    db = make_db()
    sf = make_sf()
    data = MagicMock()
    data.model_dump.return_value = {}
    session_obj = MagicMock()
    formateur_obj = make_formateur(role="stagiaire")
    db.query.return_value.filter.return_value.first.side_effect = [session_obj, formateur_obj]

    with patch.object(SessionsFormateursService, "get", return_value=sf):
        with pytest.raises(ValueError, match="formateurs"):
            SessionsFormateursService.update(db, 1, 10, data)

def test_update_raises_if_duplicate_assignment():
    db = make_db()
    sf = make_sf()
    data = MagicMock()
    data.model_dump.return_value = {"session_id": 2, "formateur_id": 10}
    session_obj = MagicMock()
    formateur_obj = make_formateur(role="formateur")
    db.query.return_value.filter.return_value.first.side_effect = [session_obj, formateur_obj]

    with patch.object(SessionsFormateursService, "get", side_effect=[sf, make_sf()]):
        with pytest.raises(ValueError, match="existe déjà"):
            SessionsFormateursService.update(db, 1, 10, data)

def test_update_success():
    db = make_db()
    sf = make_sf()
    data = MagicMock()
    data.model_dump.return_value = {}
    session_obj = MagicMock()
    formateur_obj = make_formateur(role="formateur")
    db.query.return_value.filter.return_value.first.side_effect = [session_obj, formateur_obj]

    with patch.object(SessionsFormateursService, "get", return_value=sf):
        result = SessionsFormateursService.update(db, 1, 10, data)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(sf)
    assert result is sf

def test_delete_returns_true_on_success():
    db = make_db()
    with patch.object(SessionsFormateursService, "get", return_value=make_sf()):
        assert SessionsFormateursService.delete(db, 1, 10) is True
    db.delete.assert_called_once()
    db.commit.assert_called_once()

def test_delete_returns_none_if_not_found():
    db = make_db()
    with patch.object(SessionsFormateursService, "get", return_value=None):
        assert SessionsFormateursService.delete(db, 1, 10) is None
    db.delete.assert_not_called()