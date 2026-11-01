from datetime import datetime, timezone
from typing import Any

from supabase import Client, create_client

from config import SUPABASE_KEY, SUPABASE_URL
from core.helpers import with_retry

# Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------------------------------------------------------------

# Obtém todas as tarefas determinadas na etapa
@with_retry(max_attempts=2)
def get_active_projects_by_stage(stage: str) -> list[Any]:
    return (
        supabase.table("projects")
        .select("*")
        .eq("current_stage", stage)
        .eq("status", "active")
        .execute()
        .data
    )

# Atualiza o status, ID e etapa do projeto
@with_retry(max_attempts=2)
def update_project(project_id: str, new_stage: str, new_task_id: str, new_task_id_b: str | None = None) -> None:
    data = {
        "current_stage": new_stage,
        "task_id": new_task_id,
        "started_at": datetime.now(timezone.utc),
    }
    if new_task_id_b:
        data["task_id_b"] = new_task_id_b
    supabase.table("projects").update(data).eq("id", project_id).execute()

# ------------------------------------------------------------------------------

# Cria uma bifurcação nas tarefas de CRM e IA
@with_retry(max_attempts=2)
def insert_project_branch(original: dict, stage: str, task_id: str) -> None:
    supabase.table("projects").insert({
        "company_name": original["company_name"],
        "client_name": original.get("client_name", ""),
        "current_stage": stage,
        "task_id": task_id,
        "status": "active",
        "started_at": datetime.now(timezone.utc).isoformat(),
    }).execute()

# Obtém todos os projetos concluídos
@with_retry(max_attempts=2)
def get_completed_projects_by_stage(stage: str) -> list[Any]:
    return (
        supabase.table("projects")
        .select("*")
        .eq("current_stage", stage)
        .eq("status", "completed")
        .execute()
        .data
    )

# Atualiza projetos concluídos
@with_retry(max_attempts=2)
def update_completed_project(project_id: str, new_stage: str, new_task_id: str, new_task_id_b: str | None = None) -> None:
    data = {
        "current_stage": new_stage,
        "task_id": new_task_id,
        "status": "completed",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "first_delivery_at": datetime.now(timezone.utc).isoformat(),
    }
    if new_task_id_b:
        data["task_id_b"] = new_task_id_b
    supabase.table("projects").update(data).eq("id", project_id).execute()