from constants import Pipeline, RoleAssignees, get_due_date
from core.helpers import msg_error
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA 2 - UI/UX: agendamento da reunião de apresentação do MVP do projeto

def create_stage_2(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 2 Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 3 dias a partir da criação
    data = get_due_date(3)

# ----------------------------------------------------------------------------------------------------------------------------------------------

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Reunião de MVP - {project['company_name']}",
        status=Pipeline.ETAPA_2,
        description=(
            f"O cliente {project['client_name']} deu o segundo passo\n\n\n"
            f"Necessário marcar e realizar reunião de MVP"),
        assignees=RoleAssignees.UI_UX,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 2", project["company_name"], project["client_name"], "Falha ao criar a tarefa Reunião de MVP no ClickUp"))
        return None
    
    task_id = task["id"]

    logger.info(f"Etapa 2 iniciada - {project['company_name']} - Task-Id: {task_id}")
    return task_id
