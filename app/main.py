from fastapi import FastAPI
from app.api.endpoints import auth, secrets

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(secrets.router, prefix="/secrets", tags=["secrets"])
