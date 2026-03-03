import pytest
from unittest.mock import MagicMock, patch
from app.services.user_service import UserService


def make_db():
    db = MagicMock()
    db.query.return_value.all.return_value = []
    db.query.return_value.filter.return_value.first.return_value = None
    return db

def make_user(**kwargs):
    user = MagicMock()
    user.id = kwargs.get("id", 1)
    user.email = kwargs.get("email", "jean@example.com")
    return user

def make_user_data(**kwargs):
    data = MagicMock()
    data.nom = kwargs.get("nom", "Dupont")
    data.prenom = kwargs.get("prenom", "Jean")
    data.email = kwargs.get("email", "jean@example.com")
    data.role = kwargs.get("role", "user")
    data.password = kwargs.get("password", "secret123")
    return data

def test_get_all_returns_users():
    db = make_db()
    users = [make_user(id=1), make_user(id=2)]
    db.query.return_value.all.return_value = users
    assert UserService.get_all(db) == users

def test_get_by_id_found():
    db = make_db()
    user = make_user(id=1)
    db.query.return_value.filter.return_value.first.return_value = user
    assert UserService.get_by_id(db, 1) is user

def test_get_by_id_not_found():
    db = make_db()
    assert UserService.get_by_id(db, 999) is None

def test_hash_password_differs_from_plain():
    with patch("app.services.user_service.pwd_context") as mock_ctx:
        mock_ctx.hash.return_value = "$2b$hashed"
        result = UserService.hash_password("pw")
        assert result != "pw"
        mock_ctx.hash.assert_called_once_with("pw")

def test_hash_password_is_verifiable():
    with patch("app.services.user_service.pwd_context") as mock_ctx:
        mock_ctx.hash.return_value = "$2b$hashed"
        mock_ctx.verify.return_value = True
        hashed = UserService.hash_password("pw")
        assert mock_ctx.verify("pw", hashed)

def test_create_hashes_password_and_commits():
    db = make_db()
    user_data = make_user_data(password="plain")
    with patch.object(UserService, "hash_password", return_value="hashed") as mock_hash:
        UserService.create(db, user_data)
        mock_hash.assert_called_once_with("plain")
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_update_returns_none_if_user_not_found():
    db = make_db()
    with patch.object(UserService, "get_by_id", return_value=None):
        assert UserService.update(db, 99, MagicMock()) is None

def test_update_hashes_password_field():
    db = make_db()
    user = make_user()
    user_data = MagicMock()
    user_data.model_dump.return_value = {"password": "newpass"}
    with patch.object(UserService, "get_by_id", return_value=user), \
         patch.object(UserService, "hash_password", return_value="hashed_new") as mock_hash:
        UserService.update(db, 1, user_data)
        mock_hash.assert_called_once_with("newpass")
    assert user.hashed_password == "hashed_new"

def test_delete_returns_true_on_success():
    db = make_db()
    with patch.object(UserService, "get_by_id", return_value=make_user()):
        assert UserService.delete(db, 1) is True

def test_delete_returns_none_if_user_not_found():
    db = make_db()
    with patch.object(UserService, "get_by_id", return_value=None):
        assert UserService.delete(db, 99) is None