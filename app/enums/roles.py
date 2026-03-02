from enum import Enum

class Roles(str, Enum):
    admin = "admin"
    formateur = "formateur"
    apprenant = "apprenant"