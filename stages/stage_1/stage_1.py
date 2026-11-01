from datetime import datetime, timezone

from constants import ProjectStatus, RoleAssignees, Stages, TaskStatus, get_due_date
from core.database import supabase
from core.logger import get_logger
from integrations.clickup import create_subtask, create_task

logger = get_logger(__name__)

# ETAPA: 1 - Boas-Vindas, Apresentação da Equipe, Feedback da Reunião de Vendas e Marcar Onboarding com Cliente

def run(client_name: str, company_name: str) -> dict | None:

    # Histórico do projeto no log
    logger.info(f"Etapa 1 Iniciada - {company_name}")

    # Data de vencimento da tarefa, 3 dias a partir da criação
    data = get_due_date(3)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Primeiro Passo de - {company_name}",
        status=TaskStatus.TAREFAS_CS,
        description=(
            f"O cliente {client_name} iniciou o projeto\n\n\n"
            f"Os próximos passos são:\n"
            f"Boas-Vindas\n"
            f"Apresentação da Equipe\n"
            f"Feedback da Reunião de Vendas\n"
            f"Marcar Onboarding com Cliente"),
        assignees=RoleAssignees.GESTOR,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(f"Erro na Etapa 1 - Empresa {company_name}, Cliente {client_name}")
        return None
    
    task_id = task["id"]

# ----------------------------------------------------------------------------------------------------------------------------------------------

    # Dados de cada subtarefa
    BOAS_VINDAS = {
        "name": "Boas-Vindas",
        "description": (
            "1- Adicionar todos ao grupo\n"
            "2- Dar as Boas vindas para o cliente:\n\n"
            "Boa tarde cliente!\n"
            "Sejam muito bem vindos e parabéns pela decisão.🎉🎉🎉🚀🚀🚀"
        ),
    }

    APRESENTACAO_EQUIPE = {
        "name": "Apresentação da Equipe",
        "description": (
            "3- Apresentar a equipe:\n\n\n"
            "Gostaria de apresentar oficialmente nosso time:\n\n"
            "🚀 Estratégia e Liderança: @Pedro , nosso Founder, acompanhará o projeto de perto com você.\n\n"
            "🤝 Comercial: @Joao.\n"
            "📱 Marketing & Social: @Joao Social Selling.\n\n"
            "⚙️ Tecnologia: @Felipe, @Marcos e @Isaac são nossa célula de TI dedicada.\n\n"
            "📋 Gestão e Sucesso: Eu sou o Gestor de Projetos "
            "e estaremos ao seu lado durante toda a jornada para garantir os melhores resultados."
        ),
    }

    SUBTASKS = [
        BOAS_VINDAS,
        APRESENTACAO_EQUIPE,
    ]

# ----------------------------------------------------------------------------------------------------------------------------------------------

    # Criar as subtarefas no ClickUp
    falhas = []
    for subtask in SUBTASKS:
        resultado = create_subtask(
            parent_task_id=task_id,
            name=subtask["name"],
            description=subtask.get("description", ""),
            assignees=RoleAssignees.GESTOR,
            due_date=data
        )
        if resultado is None:
            falhas.append(subtask["name"])

    if falhas:
        raise RuntimeError(
            f"Falha ao criar subtarefa(s) no ClickUp para a tarefa '{task_id}': {', '.join(falhas)}"
        )


    # Salvar o projeto no Supabase
    try:
            supabase.table("projects").insert({
                "client_name": client_name,
                "company_name": company_name,
                "task_id": task_id,
                "current_stage": Stages.STAGE_1,
                "status": ProjectStatus.ACTIVE,
                "created_at": datetime.now(timezone.utc).isoformat(),  
                "started_at": datetime.now(timezone.utc).isoformat(),
            }).execute()

            # Se der certo, logar a informação de sucesso
            logger.info(f"Projeto - {company_name} salvo no Supabase - Task-Id: {task_id}")

    except Exception as e:

        # Se der erro, logar a informação de erro
        logger.error(f"Erro ao salvar Etapa 1 no Supabase - {company_name}: {e}")


        