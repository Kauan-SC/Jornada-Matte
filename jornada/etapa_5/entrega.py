from constants import Pipeline, RoleAssignees, get_due_date
from core.helpers import msg_error
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA 5 - Entrega: conexão de teste e reunião de entrega final da IA

def create_stage_3d(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 5 Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 3 dias a partir da criação
    data = get_due_date(3)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Realizar entrega Final da IA - {project['company_name']}",
        status=Pipeline.ETAPA_5,
        description=(
        "[ ] Conexão de Teste: Conectar um número de WhatsApp provisório para realizar os testes da IA.\n\n"
        "[ ] Reunião de Apresentação: Agendar a reunião de entrega com o cliente para demonstrar a IA em funcionamento e apresentar o documento de validação."),
        assignees=RoleAssignees.GESTOR,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 5", project["company_name"], project["client_name"], "Falha ao criar a tarefa Entrega no ClickUp"))
        return None

    task_id = task["id"]
    logger.info(f"Etapa 5 iniciada - {project['company_name']} - Task-Id: {task_id}")
    return task_id
