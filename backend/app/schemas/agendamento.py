from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional


class AgendamentoCreate(BaseModel):
    nome_cliente: str
    telefone: str
    email: Optional[EmailStr] = None

    placa: str
    modelo_veiculo: str
    ano_veiculo: int

    descricao_problema: str

    data_agendamento: date
    horario: time

class AtualizarStatus(BaseModel):
    status: str