from fastapi import FastAPI
from app.routes import user_routes, formation_routes, session_routes, inscription_routes

app = FastAPI(title="Simplon Training API")

app.include_router(user_routes.router)
app.include_router(formation_routes.router)
app.include_router(session_routes.router)
app.include_router(inscription_routes.router)