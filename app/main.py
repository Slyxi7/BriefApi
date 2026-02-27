from fastapi import FastAPI
from app.routers import user_router, formation_router, session_router, inscription_router, sessions_formateur_router

app = FastAPI(title="Simplon Training API")

app.include_router(user_router.router)
app.include_router(formation_router.router)
app.include_router(session_router.router)
app.include_router(inscription_router.router)
app.include_router(sessions_formateur_router.router)