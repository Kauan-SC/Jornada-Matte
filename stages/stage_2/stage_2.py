from constants import RoleAssignees, TaskStatus, get_due_date
from core.logger import get_logger
from integrations.clickup import create_subtask, create_task

logger = get_logger(__name__)

# ETAPA: 2 - Pós-Onboarding, Enviar Instruções de Criação de Conta no CRM e Feedback da Reunião de Onboarding

def create_stage_2(project: dict) -> str | None:

    logger.info(f"Etapa 2 Iniciada - {project['company_name']}")

    data = get_due_date(3)

# Cria a tarefa principal da Etapa 2 no ClickUp
    task = create_task(
        name=f"Pós-Onboarding de - {project['company_name']}",
        status=TaskStatus.TAREFAS_CS,
        description=(
            f"O cliente {project['client_name']} deu o segundo passo\n\n\n"
            f"Enviar instruções sobre criação de conta no CRM\n"),
        assignees=RoleAssignees.GESTOR,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(f"Erro na Etapa 2 - {project['company_name']}")
        return None
    
    task_id = task["id"]

# ----------------------------------------------------------------------------------------------------------------------------------------------

    # Dados de cada subtarefa
    MARCAR_ONBOARDING = {
        "name": "Marcar Onboarding com Cliente",
        "description": (
            "1- Marcar o Onboarding de Apresentação com o cliente\n\n"
        ),
    }

    SUBTASKS = [MARCAR_ONBOARDING]

# ----------------------------------------------------------------------------------------------------------------------------------------------

    # Criar cada subtarefa da Etapa 2 no ClickUp
    for subtask in SUBTASKS:
        create_subtask(
            parent_task_id=task_id,
            name=subtask["name"],
            description=subtask.get("description", ""),
            assignees=RoleAssignees.GESTOR,
            due_date=data
            )

    logger.info(f"Etapa 2 iniciada - {project['company_name']} - Task-Id: {task_id}")
    return task_id
       
