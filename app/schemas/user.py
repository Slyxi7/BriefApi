import re
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from enums.roles import Roles

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: Roles
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


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Roles] = None

class UserRead(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr
    role: Roles
    date_inscription: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDelete(BaseModel):
    hard: bool = False