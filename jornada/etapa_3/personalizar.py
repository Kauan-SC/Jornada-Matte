from constants import Pipeline, RoleAssignees, get_due_date
from core.helpers import msg_error
from core.logger import get_logger
from integrations.clickup import create_task

logger = get_logger(__name__)

# ETAPA 3 - Personalizar: briefing de personalização da plataforma (acessos, leads, WhatsApp, captação e IA)

def create_stage_3a(project: dict) -> str | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 3(Personalizar) Iniciada - {project['company_name']}")

    # Data de vencimento da tarefa, 10 dias a partir da criação
    data = get_due_date(10)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Personalizar a Plataforma {project['company_name']}",
        status=Pipeline.ETAPA_3,
        description=(
            f"Briefing de Personalização da plataforma - {project['company_name']}\n\n"

            f"1. Acessos e Equipe\n"
            f"- Total de usuários:\n"
            f"- Nomes e E-mails:\n\n"

            f"2. Distribuição de Leads\n"
            f"- Vendedores:\n"
            f"- Regra de distribuição:\n\n"

            f"3. WhatsApp e Canais\n"
            f"- Quantidade de números WhatsApp:\n"
            f"- Tipo de conexão:\n"
            f"- Atuação da IA em outros canais:\n\n"

            f"4. Captação e Base de Dados\n"
            f"- Tráfego Pago Ativo:\n"
            f"- Importação de Leads:\n\n"

            f"5. Funcionalidades da IA\n"
            f"- Agendamento Automático:\n\n"

            f"6. Observações Extras\n"
            f"- \n"),
        assignees=RoleAssignees.UI_UX,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 3", project["company_name"], project["client_name"], "Falha ao criar a tarefa Personalizar a Plataforma no ClickUp"))
        return None        
    
    task_id = task["id"]

    logger.info(f"Etapa 3 de Personalizar iniciada - {project['company_name']} - Task-Id: {task_id}")
    return task_id