from pydantic import BaseModel, ConfigDict

class InscriptionBase(BaseModel):
    session_id: int
    apprenant_id: int 


class InscriptionCreate(InscriptionBase):
    pass

class InscriptionUpdate(InscriptionBase):
    session_id: int | None = None
    apprenant_id: int  | None = None

class InscriptionRead(InscriptionBase):
    model_config = ConfigDict(from_attributes=True)

class InscriptionDelete(BaseModel):
    hard: bool = False