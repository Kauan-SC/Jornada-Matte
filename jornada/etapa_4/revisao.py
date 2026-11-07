
from constants import Pipeline, get_due_date
from core.helpers import get_reviewer_dev, msg_error, notify_acompanhamento
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA 4 - Revisão: checklist de validação da IA com comprovação por prints

def create_stage_3c(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 4(Revisão) Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 5 dias a partir da criação
    data = get_due_date(5)

    # Obter o responsável pela criação da IA para atribuir a tarefa de revisão
    reviewer = get_reviewer_dev(project["task_id"])

    task = create_task(
        name=f"Revisão da IA - {project['company_name']}",
        status=Pipeline.ETAPA_4,
        description=(
        "Checklist de Revisão da IA\n\n"

        "[ ] Atendimento de ponta a ponta: Validar a jornada completa da IA com o lead (anexar print da conversa no WhatsApp e na Plataforma).\n\n"

        "[ ] Registro e Campos (CRM): Confirmar a criação do contato e o preenchimento correto dos dados nos campos personalizados (anexar print).\n\n"

        "[ ] Pipeline Automático: Validar se a oportunidade avançou de etapa no funil automaticamente conforme a conversa.\n\n"

        "[ ] Notificações: Confirmar se o alerta de atendimento foi acionado para o consultor (anexar print).\n\n"

        "Entregável Obrigatório\n"
        "Reúna todos os prints de comprovação em um documento consolidado e suba para o github"),
        assignees=reviewer,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 4", project["company_name"], project["client_name"], "Falha ao criar a tarefa Revisão no ClickUp"))
        return None        
    
    task_id = task["id"]
    notify_acompanhamento(
        f"🧐{project['company_name']} está na etapa de Revisar a IA",
        f"Task-Id: {task_id}",
    )
    return task_id