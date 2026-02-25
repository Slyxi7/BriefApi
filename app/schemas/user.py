import re
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

ROLES = ["admin", "formateur", "apprenant"]

class UserBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: str
   
    @field_validator("role")
    def validate_role(cls, val):
        if val not in ROLES:
            raise ValueError(f"Rôle invalide. Choisir parmi : {ROLES}")
        return val

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, val):
        if len(val) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        
        if not re.search(r"[A-Z]", val):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")

        if not re.search(r"[a-z]", val):
            raise ValueError("Le mot de passe doit contenir au moins une minuscule")
        
        if not re.search(r"[0-9]", val):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", val):
            raise ValueError("Le mot de passe doit contenir au moins un symbole")
        return val


class UserUpdate(UserBase):
    nom: str | None = None
    prenom: str | None = None
    email: EmailStr | None = None
    role: str | None = None

    @field_validator("role")
    def validate_role(cls, val):
        if val is None:
            return val
        if val not in ROLES:
            raise ValueError(f"Rôle invalide. Choisir parmi : {ROLES}")
        return val

class UserRead(UserBase):
    id: int
    date_inscription: datetime

    class Config: from_attributes = True

class UserDelete(BaseModel):
    hard: bool = False