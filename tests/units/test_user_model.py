import pytest
from app.schemas.user import UserCreate, UserUpdate, UserRead
from pydantic import ValidationError
from datetime import datetime


def test_user_create_valid():
    dto = UserCreate(
        nom="Doe",
        prenom="John",
        email="john@doe.com",
        role="admin",
        password="SuperSecure1!"
    )

    assert dto.nom == "Doe"
    assert dto.prenom == "John"
    assert dto.email == "john@doe.com"
    assert dto.role == "admin"
    assert dto.password == "SuperSecure1!"


def test_user_create_invalid_role():
    with pytest.raises(ValidationError):
        UserCreate(
            nom="Doe",
            prenom="John",
            email="john@doe.com",
            role="invalid_role"
        )


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            nom="Doe",
            prenom="John",
            email="not-an-email",
            role="admin"
        )


def test_user_update_valid_partial():
    dto = UserUpdate(role="formateur")
    assert dto.role == "formateur"


def test_user_update_invalid_role():
    with pytest.raises(ValidationError):
        UserUpdate(role="invalid")


def test_user_update_empty_ok():
    UserUpdate() 
    assert True

def test_user_read_valid():
    dto = UserRead(
        id=1,
        nom="Doe",
        prenom="John",
        email="john@doe.com",
        role="admin",
        date_inscription=datetime.now()
    )
    assert dto.id == 1