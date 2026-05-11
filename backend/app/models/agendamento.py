from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime
from datetime import datetime

from app.database.connection import Base


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)

    nome_cliente = Column(String(100), nullable=False)

    telefone = Column(String(20), nullable=False)

    email = Column(String(100), nullable=True)

    placa = Column(String(10), nullable=False)

    modelo_veiculo = Column(String(100), nullable=False)

    ano_veiculo = Column(Integer, nullable=False)

    descricao_problema = Column(Text, nullable=False)

    data_agendamento = Column(Date, nullable=False)

    horario = Column(Time, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="PENDENTE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )