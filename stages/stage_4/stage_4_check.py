from constants import Stages
from core.database import get_active_projects_by_stage, update_completed_project
from core.logger import get_logger
from integrations.clickup import is_task_completed

logger = get_logger(__name__)

# Verifica se os projetos estão concluídos usando o ID para obter as informações da tarefa
def check_stage_4a() -> None:
    projects = get_active_projects_by_stage(Stages.STAGE_4)

    for project in projects:
        if is_task_completed(project["task_id"]):
            logger.info(f"Projeto {project['company_name']}: Etapa 4 concluida. Personalização do CRM concluida!")

            update_completed_project(project["id"], Stages.FINAL_STAGE_CRM, project["task_id"])
