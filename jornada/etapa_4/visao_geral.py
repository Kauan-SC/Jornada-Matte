from constants import Pipeline, RoleAssignees, get_due_date
from core.helpers import msg_error
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA 4 - Visão Geral: treinamento da equipe na plataforma

def create_stage_4a(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 4(Visão Geral) Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 3 dias a partir da criação
    data = get_due_date(3)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Visão Geral da Plataforma - {project['company_name']}",
        status=Pipeline.ETAPA_4,
        description=(
            "- Marcar treinamento com a equipe.\n"),
        assignees=RoleAssignees.UI_UX,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 4", project["company_name"], project["client_name"], "Falha ao criar a tarefa Visão Geral no ClickUp"))
        return None
    
    task_id = task["id"]

    logger.info(
        f"{project['company_name']} está na etapa de Visão Geral - Task-Id: {task_id}",
    )
    return task_id