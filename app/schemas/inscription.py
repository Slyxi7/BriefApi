from pydantic import BaseModel, ConfigDict
from typing import Optional

class InscriptionBase(BaseModel):
    session_id: int
    apprenant_id: int 


class InscriptionCreate(InscriptionBase):
    pass

class InscriptionUpdate(InscriptionBase):
    session_id: Optional[int] = None
    apprenant_id: Optional[int] = None

class InscriptionRead(InscriptionBase):
    model_config = ConfigDict(from_attributes=True)

class InscriptionDelete(BaseModel):
    hard: bool = False