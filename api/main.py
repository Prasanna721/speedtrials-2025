from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import systems

app = FastAPI(
    title="Georgia Water Watch API",
    description="API for accessing Georgia's public water system data.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(systems.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Georgia Water Watch API"}