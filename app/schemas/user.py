import re
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from app.enums.roles import Roles

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: Roles
    password: str

    @field_validator("password")
    def validate_password(cls, val):
        if len(val) < 8:
            raise ValueError("Password must contain at least 8 characters")
        
        if not re.search(r"[A-Z]", val):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", val):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r"[0-9]", val):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", val):
            raise ValueError("Password must contain at least one symbol")
        
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