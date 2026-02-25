from enum import Enum

class Roles(str, Enum):
    debutant = "admin",
    intermediaire = "formateur"
    avance = "apprenant"