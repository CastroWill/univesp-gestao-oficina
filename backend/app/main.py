from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.connection import engine
from backend.app.models.agendamento import Agendamento
from backend.app.routes.agendamento import router as agendamento_router


Agendamento.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestão Oficina",
    description="Sistema de gerenciamento de oficina",
    version="1.0.0"
)


origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agendamento_router)


@app.get("/")
def home():
    return {
        "mensagem": "API funcionando!"
    }