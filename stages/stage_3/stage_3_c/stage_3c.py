import random

from constants import RoleAssignees, TaskStatus, get_due_date
from core.helpers import notify_acompanhamento
from core.logger import get_logger
from integrations.clickup import create_task, get_task

logger = get_logger(__name__)

# ETAPA: 3C - Revisão da IA

def get_reviewer_dev(task_id_3b: str) -> list[int]:
    task = get_task(task_id_3b)
    if task is None:
        return [random.choice(RoleAssignees.DEVS)]
    
    assignee_ids = {a["id"]for a in task.get("assignees", [])}
    other_devs = [dev for dev in RoleAssignees.DEVS if dev not in assignee_ids]

    return [random.choice(other_devs)] if other_devs else [random.choice(RoleAssignees.DEVS)]

# Criar Tarefa - Terceira Etapa - Verificação da IA
def create_stage_3c(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 3C Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 5 dias a partir da criação
    data = get_due_date(5)

    # Obter o responsável pela Etapa 3B para atribuir a tarefa de revisão da IA
    reviewer = get_reviewer_dev(project["task_id"])

    task = create_task(
        name=f"Revisão da IA - {project['company_name']}",
        status=TaskStatus.TAREFAS_DEV,
        description=(
        "Checklist de Revisão da IA\n\n"
        
        "- Atendimento completo: A IA precisa atender o lead de ponta a ponta (incluir print do teste completo).\n\n"

        "- Registros de sistema: Capturar prints das conversas no WhatsApp e do registro no CRM.\n\n"

        "- Campos personalizados: Validar se os dados foram preenchidos corretamente no CRM.\n\n"

        "- Notificações: Confirmar o envio de alerta para o consultor (incluir print da notificação).\n\n"

        "- Pipeline automática: Garantir que a oportunidade seja movida de etapa automaticamente conforme o avanço do contato.\n\n"
        
        "Importante: As imagens de comprovação são obrigatórias. Após coletar os prints, monte um documento consolidado e envie no grupo do cliente para atestar o funcionamento da IA."),
        assignees=reviewer,
        due_date=data
    )

    # Se a criação da Etapa 3C falhar, logar o erro e continuar com o próximo projeto
    if task is None:
        logger.error(f"Erro na Etapa 3C - {project['company_name']}")
        return None
    
    task_id = task["id"]
    notify_acompanhamento(
        f"🧐{project['company_name']} está na etapa de Revisar a IA",
        f"Task-Id: {task_id}",
    )
    return task_id