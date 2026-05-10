from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.agendamento import Agendamento
from app.schemas.agendamento import (
    AgendamentoCreate,
    AtualizarStatus
)

from typing import Optional
from sqlalchemy import or_, func
from datetime import datetime

from datetime import date
from app.services.disponibilidade import (
    HORARIOS_PADRAO,
    formatar_horario
)

router = APIRouter()


@router.post("/agendamentos")
def criar_agendamento(
    agendamento: AgendamentoCreate,
    db: Session = Depends(get_db)
):

    conflito = db.query(Agendamento).filter(
        Agendamento.data_agendamento == agendamento.data_agendamento,
        Agendamento.horario == agendamento.horario
    ).first()

    if conflito:
        raise HTTPException(
            status_code=400,
            detail="Horário indisponível"
        )

    novo_agendamento = Agendamento(
        nome_cliente=agendamento.nome_cliente,
        telefone=agendamento.telefone,
        email=agendamento.email,
        placa=agendamento.placa,
        modelo_veiculo=agendamento.modelo_veiculo,
        ano_veiculo=agendamento.ano_veiculo,
        descricao_problema=agendamento.descricao_problema,
        data_agendamento=agendamento.data_agendamento,
        horario=agendamento.horario,
        status="PENDENTE"
    )

    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)

    return {
        "mensagem": "Agendamento criado com sucesso",
        "id": novo_agendamento.id
    }

@router.get("/horarios-disponiveis")
def listar_horarios_disponiveis(
    data: date,
    db: Session = Depends(get_db)
):

    agendamentos = db.query(Agendamento).filter(
        Agendamento.data_agendamento == data
    ).all()

    horarios_ocupados = {
        agendamento.horario
        for agendamento in agendamentos
    }

    horarios_disponiveis = [
        formatar_horario(horario)
        for horario in HORARIOS_PADRAO
        if horario not in horarios_ocupados
    ]

    return horarios_disponiveis

@router.get("/agendamentos")
def listar_agendamentos(
    db: Session = Depends(get_db),
    data: Optional[date] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
):

    query = db.query(Agendamento)

    # filtro por data
    if data:
        query = query.filter(
            Agendamento.data_agendamento == data
        )

    # filtro por status
    if status:
        query = query.filter(
            Agendamento.status == status.upper()
        )

    # busca
    if search:
        query = query.filter(
            or_(
                Agendamento.nome_cliente.ilike(f"%{search}%"),
                Agendamento.email.ilike(f"%{search}%"),
                Agendamento.telefone.ilike(f"%{search}%")
            )
        )

    agendamentos = query.order_by(
        Agendamento.data_agendamento,
        Agendamento.horario
    ).all()

    return agendamentos

@router.patch("/agendamentos/{agendamento_id}/status")
def atualizar_status(
    agendamento_id: int,
    dados: AtualizarStatus,
    db: Session = Depends(get_db)
):

    status_validos = [
        "PENDENTE",
        "CONFIRMADO",
        "CONCLUIDO",
        "CANCELADO"
    ]

    status = dados.status.upper()

    if status not in status_validos:
        raise HTTPException(
            status_code=400,
            detail="Status inválido"
        )

    agendamento = db.query(Agendamento).filter(
        Agendamento.id == agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(
            status_code=404,
            detail="Agendamento não encontrado"
        )

    agendamento.status = status

    db.commit()
    db.refresh(agendamento)

    return {
        "mensagem": "Status atualizado com sucesso",
        "status": agendamento.status
    }

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    hoje = datetime.today().date()

    total = db.query(Agendamento).count()

    pendentes = db.query(Agendamento).filter(
        Agendamento.status == "PENDENTE"
    ).count()

    confirmados = db.query(Agendamento).filter(
        Agendamento.status == "CONFIRMADO"
    ).count()

    hoje_count = db.query(Agendamento).filter(
        Agendamento.data_agendamento == hoje
    ).count()

    return {
        "total": total,
        "pendentes": pendentes,
        "confirmados": confirmados,
        "hoje": hoje_count
    }