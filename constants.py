# Status do Projeto
from datetime import datetime, timedelta
from typing import ClassVar
from zoneinfo import ZoneInfo


class ProjectStatus:
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# Etapas do Projeto
class Stages:
    STAGE_1 = "stage_1"
    STAGE_2 = "stage_2"
    STAGE_3A = "stage_3_a"
    STAGE_3B = "stage_3_b"
    STAGE_3C = "stage_3_c"
    STAGE_3D = "stage_3_d"
    STAGE_4 = "stage_4"
    FINAL_STAGE_CRM = "final_stage_CRM"
    FINAL_STAGE_IA = "final_stage_IA"

# Etapas do Projeto | V2
class Etapas:
    ETAPA_1 = "Apresentação"
    ETAPA_2 = "Reunião com UI/UX"
    ETAPA_3_PERSONALIZAR = "Personalizar Plataforma"
    ETAPA_3_CRIAR = "Criar IA"
    ETAPA_4_REVISAO = "Revisão da IA"
    ETAPA_4_VISAO_GERAL = "Visão Geral da Plataforma"
    ETAPA_5 = "Entrega Final"


# Pipelines do ClickUp | V2
class Pipeline:
    ETAPA_1 = "ETAPA 1 - APRESENTAÇÃO"
    ETAPA_2 = "ETAPA 2 - UI/UX"
    ETAPA_3 = "ETAPA 3 - PERSONALIZAR E CRIAR"
    ETAPA_4 = "ETAPA 4 - REVISAR E VISÃO GERAL"
    ETAPA_5 = "ETAPA 5 - ENTREGA FINAL"
    COMPLETE = "COMPLETE"

# Pipelines do ClickUp
class TaskStatus:
    ABERTAS = "ABERTAS"
    AGUARDANDO_RESPOSTA = "AGUARDANDO RESPOSTA"
    PROJETO_FINALIZADO = "PROJETO FINALIZADO"
    REUNIOES_PEDRO = "REUNIÕES PEDRO"
    REUNIOES_KAUAN = "REUNIÕES KAUAN"
    PERSONALIZAR_CRM = "PERSONALIZAR CRM - CS"
    TAREFAS_CS = "TAREFAS DO CS"
    TAREFAS_DEV = "CRIAR IA"
    TAREFAS_DE_SUPORTE = "TAREFAS DE SUPORTE"
    COMPLETE = "COMPLETE"

# Cargos dos Funcionários
class EmployeeRoles:
    DEV = "Desenvolvedor"
    GESTOR = "Gestor de Projetos"

# ID dos Membros do ClickUp
class ClickUpMembers:
    # Founder
    PEDRO     = 72844227

    # Desenvolvedores
    ISAAC     = 111975410
    FELIPE    = 118035447

    # UI/UX
    MARCOS_EDUARDO  = 101717627

    # Gestor de Projetos
    KAUAN     = 111975463

    # Suporte
    ENZO      = 101721965

# Mapeamento de Cargos/Responsáveis
class RoleAssignees:
    GESTOR: ClassVar[list[int]] = [ClickUpMembers.KAUAN]
    SUPORTE: ClassVar[list[int]] = [ClickUpMembers.ENZO]
    UI_UX: ClassVar[list[int]] = [ClickUpMembers.MARCOS_EDUARDO]
    DEVS: ClassVar[list[int]] = [
        ClickUpMembers.ISAAC,
        ClickUpMembers.FELIPE,
    ]

# Obtém a data de vencimento no formato timestamp
def get_due_date(days: int) -> int:
    due = datetime.now(ZoneInfo("America/Sao_Paulo"))
    days_added = 0
    while days_added < days:
        due += timedelta(days=1)
        if due.weekday() < 5:  # 0=Seg ... 4=Sex, 5=Sab, 6=Dom
            days_added += 1
    return int(due.timestamp() * 1000)