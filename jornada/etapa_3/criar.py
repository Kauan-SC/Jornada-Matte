from constants import Pipeline, get_due_date
from core.helpers import msg_error, notify_acompanhamento
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA 3 - Criar: criação da IA a partir do MVP enviado

def create_stage_3b(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 3(Criar) Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 15 dias a partir da criação
    data = get_due_date(15)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Criação da IA - {project['company_name']}",
        status=Pipeline.ETAPA_3,
        description=(
        "Criar a IA: \n"

        "MVP será enviado"),
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 3", project["company_name"], project["client_name"], "Falha ao criar a tarefa Criar IA no ClickUp"))
        return None        
    
    task_id = task["id"]

    notify_acompanhamento(
        f"{project['company_name']} está na etapa de criar IA",
        f"Task-Id: {task_id}",
    )

    return task_id
    
