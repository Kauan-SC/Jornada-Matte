import logging
import random
import sys
import time
from collections.abc import Callable
from functools import wraps

import requests

from config import DISCORD_WEBHOOK_URL_ACOMPANHAMENTO
from constants import RoleAssignees
from integrations.clickup import get_task, is_task_completed

logger = logging.getLogger(__name__)

# Retry para Supabase
def with_retry(max_attempts: int = 2, delay_seconds: float = 2.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(
                        f"[Supabase] Tentativa {attempt}/{max_attempts} falhou em {func.__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            logger.error(f"[Supabase] Falha definitiva em {func.__name__} após {max_attempts} tentativas - AÇÃO MANUAL NECESSÁRIA: {last_exc}")
            assert last_exc is not None
            raise last_exc
        return wrapper
    return decorator

# ------------------------------------------------------------------------------

#  Padrão p/ mensagem de Error
def msg_error(stage: str, company_name: str, client_name: str, motivo: str, task_id: str | None = None) -> str:
    base = f"[{stage}] Falha - Empresa: {company_name} | Cliente: {client_name}"
    if task_id:
        base += f" | Task ID: {task_id}"
    return f"{base} | Motivo: {motivo}"

# ------------------------------------------------------------------------------

# Mensagem em formato Embed para Discord
IS_COMPONENTS_V2 = 1 << 15

def _text(content: str) -> dict:
    return {"type": 10, "content": content}

def _divider() -> dict:
    return {"type": 14, "spacing": 1, "divider": True}

def notify_acompanhamento(*lines: str) -> None:
    if not DISCORD_WEBHOOK_URL_ACOMPANHAMENTO:
        return

    components = []
    for i, line in enumerate(lines):
        if i > 0:
            components.append(_divider())
        components.append(_text(line))

    payload = {
        "flags": IS_COMPONENTS_V2,
        "components": [
            {
                "type": 17,
                "components": components,
            }
        ],
    }

    try:
        resp = requests.post(DISCORD_WEBHOOK_URL_ACOMPANHAMENTO, json=payload, timeout=5.0)
        if resp.status_code not in (200, 204, 429):
            print(f"Discord notify_acompanhamento falhou: {resp.status_code}: {resp.content}", file=sys.stderr)
    except Exception as e:
        print(f"Erro ao enviar notify_acompanhamento para o Discord: {e}", file=sys.stderr)

# ------------------------------------------------------------------------------

def get_reviewer_dev(task_id_3b: str) -> list[int]:
    task = get_task(task_id_3b)
    if task is None:
        return [random.choice(RoleAssignees.DEVS)]
    
    assignee_ids = {a["id"]for a in task.get("assignees", [])}
    other_devs = [dev for dev in RoleAssignees.DEVS if dev not in assignee_ids]

    return [random.choice(other_devs)] if other_devs else [random.choice(RoleAssignees.DEVS)]

# ------------------------------------------------------------------------------

# Verificador Simples
def checker(
    current_stage: str,
    next_stage: str,
    create_next_stage: Callable[[dict], str | None],
) -> None:
    from core.database import get_active_projects_by_stage, update_project

    projects = get_active_projects_by_stage(current_stage)

    for project in projects:
        if not is_task_completed(project["task_id"]):
            continue

        new_task_id = create_next_stage(project)

        if new_task_id is None:
            logger.error(msg_error(current_stage, project["company_name"], project["client_name"], f"Falha ao criar próxima etapa ({next_stage})"))
            continue

        update_project(project["id"], next_stage, new_task_id)

# ------------------------------------------------------------------------------

# Verificador Duplo
def checker_duo(
    current_stage: str,
    branch_a: tuple[str, Callable[[dict], str | None]],
    branch_b: tuple[str, Callable[[dict], str | None]],
) -> None:
    from core.database import (
        get_active_projects_by_stage,
        insert_project_branch,
        update_project,
    )

    projects = get_active_projects_by_stage(current_stage)

    for project in projects:
        if not is_task_completed(project["task_id"]):
            continue

        stage_a, create_a = branch_a
        stage_b, create_b = branch_b

        task_id_a = create_a(project)
        task_id_b = create_b(project)

        if task_id_a is None or task_id_b is None:
            logger.error(msg_error(current_stage, project["company_name"], project["client_name"], "Falha ao criar uma das trilhas (CRM/IA)"))
            continue

        update_project(project["id"], stage_a, task_id_a)
        insert_project_branch(project, stage_b, task_id_b)

# ------------------------------------------------------------------------------

# Verificador Final
def checker_final(current_stage: str, final_stage: str) -> None:
    from core.database import get_active_projects_by_stage, update_completed_project

    projects = get_active_projects_by_stage(current_stage)

    for project in projects:
        if not is_task_completed(project["task_id"]):
            continue

        update_completed_project(project["id"], final_stage, project["task_id"])
