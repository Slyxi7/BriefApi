from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

ROLES = ["admin", "formateur", "apprenant"]

class UserBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: str

    @field_validator("role")
    def validate_role(cls, i):
        if i not in ROLES:
            raise ValueError(f"Rôle invalide. Choisir parmi : {ROLES}")
        return i

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    role: str | None = None

class UserRead(UserBase):
    id: int
    date_inscription: datetime

    class Config:
        from_attributes = True