from datetime import datetime, timezone

from constants import Pipeline, ProjectStatus, RoleAssignees, Stages, get_due_date
from core.database import supabase
from core.helpers import msg_error, notify_acompanhamento
from core.logger import get_logger
from integrations.clickup import create_subtask, create_task

logger = get_logger(__name__)

# ETAPA 1 - Apresentação: boas-vindas, apresentação da equipe e agendamento da reunião inicial

def run(client_name: str, company_name: str) -> dict | None:

    # Histórico do projeto no log
    notify_acompanhamento(f"{company_name} - Acabou de iniciar sua Jornada com a Matte")

    # Data de vencimento da tarefa, 3 dias a partir da criação
    data = get_due_date(3)

    # Criar a tarefa principal no ClickUp
    task = create_task(
        name=f"Etapa 1(Apresentação) - {company_name}",
        status=Pipeline.ETAPA_1,
        description=(
            f"{company_name} - Acabou de iniciar sua Jornada com a Matte\n\n\n"
            f"Os próximos passos são:\n"
            f"Apresentação no grupo\n"
            f"Reuniao de Apresentação"),
        assignees=RoleAssignees.GESTOR,
        due_date=data
    )

    # Se a tarefa não for criada, logar o erro e retornar None
    if task is None:
        logger.error(msg_error("Etapa 1", company_name, client_name, "Falha ao criar a tarefa Apresentação no ClickUp"))
        return None

    task_id = task["id"]

# ----------------------------------------------------------------------------------------------------------------------------------------------

    # Dados das subtarefas
    APRESENTACAO_EQUIPE = {
        "name": "Boas-Vindas e Apresentação da Equipe",
        "description": (
             
            "Olá, boa tarde! Sejam muito bem-vindos e parabéns por essa decisão incrível! 🎉 Estamos muito felizes em ter vocês com a gente.\n"

            "Gostaria de apresentar oficialmente a equipe que fará parte do seu projeto:\n\n"

            "Estratégia e Liderança: @Pedro, nosso Founder, acompanhará tudo de perto com você.\n\n"
            "🤝 Comercial: @Joao será o seu ponto de contato para alinhamentos de negócios.\n"
            "📱 Marketing e Social: @Joao comandará as nossas ações de Social Selling.\n\n"
            "⚙️ Tecnologia: @Felipe, @Marcos e @Isaac formam a nossa célula de TI dedicada.\n\n"
            "📋 Gestão e Sucesso: Eu, como Gestor de Projetos, junto com o @Enzo no Suporte, estaremos ao seu lado durante toda a jornada para garantir os melhores resultados."
        ),
    }

    REUNIAO_DE_APRESENTACAO = {
         "name": "Reunião de Apresentação",
         "description": (

              "Pessoal, para darmos início oficial ao projeto, nosso primeiro passo é agendar uma reunião de alinhamento.\n\n" 
              
              "Nela, apresentarei o cronograma e explicarei detalhadamente como funcionará cada etapa até a entrega final da IA e da plataforma.\n\n"
              
              "Como está a disponibilidade de agenda de vocês para conversarmos nesta semana?"
         )
    }

    SUBTASKS = [
        APRESENTACAO_EQUIPE, REUNIAO_DE_APRESENTACAO
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

    # Se alguma subtarefa falhar, logar o erro (a tarefa principal já foi criada, então não interrompe o fluxo)
    if falhas:
        logger.error(msg_error("Etapa 1", company_name, client_name, f"Falha ao criar Sub-tarefas: {', '.join(falhas)}", task_id)
        )

# ----------------------------------------------------------------------------------------------------------------------------------------------

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

        logger.info(f"Projeto - {company_name} salvo no Supabase - Task-Id: {task_id}")

    except Exception as e:
        # Projeto já existe no ClickUp mas não foi persistido — o checker não vai conseguir avançar essa etapa sem ajuste manual no Supabase
        logger.error(msg_error("Etapa 1", company_name, client_name, f"Falha ao salvar no Supabase: {e}", task_id))


        