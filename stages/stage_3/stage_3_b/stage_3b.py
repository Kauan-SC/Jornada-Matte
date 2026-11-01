from constants import TaskStatus, get_due_date
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA: 3B - Criação da IA

def create_stage_3b(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 3B Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 15 dias a partir da criação
    data = get_due_date(15)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Criação da IA - {project['company_name']}",
        status=TaskStatus.TAREFAS_DEV,
        description=(
        "Realizar a criaçao da IA:\n"

        "Briefing abaixo:"),
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(f"Erro na Etapa 3B - {project['company_name']}")
        return None
    
    task_id = task["id"]
    logger.info(
        f"{project['company_name']} está na etapa de criar IA - Task-Id: {task_id}",
        extra={"notify_acompanhamento": True},
    )
    
    return task_id
    
