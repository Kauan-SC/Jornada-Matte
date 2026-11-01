import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import CLICKUP_API_KEY, CLICKUP_LIST_ID
from core.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.clickup.com/api/v2"
HEADERS = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}

# Tentar novamente
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=Retry(
    total=3, backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
)))

# --------------------------------------------------------------------------------------------------------------------------------------------

# Criar Tarefa - Objeto
def create_task(name: str, description: str = "", markdown_content: str = "", assignees: list | None = None, due_date: int | None = None, status: str | None = None) -> dict | None:
    url = f"{BASE_URL}/list/{CLICKUP_LIST_ID}/task"
    payload = {
        "name": name,
        "description": description,
        "markdown_content": markdown_content,
        "assignees": assignees or [],
        "due_date": due_date
    }
    if status:
        payload["status"] = status
    try:
        response = session.post(url, json=payload, headers=HEADERS, timeout=15)
        response.raise_for_status()
        task = response.json()
        logger.info(f"Tarefa criada: {task['name']}  ID: {task['id']}")
        return task
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            logger.error(f"Erro ao criar tarefa '{name}': {e.response.status_code} - {e.response.text}")
        else:
            logger.error(f"Erro ao criar tarefa '{name}': sem resposta do ClickUp ({type(e).__name__})")
        return None

# --------------------------------------------------------------------------------------------------------------------------------------------

# Criar Sub-Tarefa - Objeto
def create_subtask(parent_task_id: str, name: str, description: str = "", markdown_content: str = "", assignees: list | None = None, due_date: int | None = None) -> dict | None:
    url = f"{BASE_URL}/list/{CLICKUP_LIST_ID}/task"
    payload = {
        "name": name,
        "description": description,
        "markdown_content": markdown_content,
        "assignees": assignees,
        "due_date": due_date,
        "parent": parent_task_id
    }
    try:
        response = session.post(url, json=payload, headers=HEADERS, timeout=15)
        response.raise_for_status()
        subtask = response.json()
        logger.info(f"Sub-tarefa criada: {subtask['name']}  ID: {subtask['id']}")
        return subtask
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            logger.error(f"Erro ao criar tarefa '{name}': {e.response.status_code} - {e.response.text}")
        else:
            logger.error(f"Erro ao criar tarefa '{name}': sem resposta do ClickUp ({type(e).__name__})")
        return None
    
# --------------------------------------------------------------------------------------------------------------------------------------------

# Obter task_id - Objeto (Obter o Id da Tarefa para a Criação de Sub-Tarefas)
def get_task(task_id: str) -> dict | None:
    url = f"{BASE_URL}/task/{task_id}"
    try:
        response = session.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        task = response.json()
        logger.info(f"Tarefa obtida: {task['name']}  ID: {task['id']}")
        return task
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            logger.error(f"Erro ao obter tarefa '{task_id}': {e.response.status_code} - {e.response.text}")
        else:
            logger.error(f"Erro ao obter tarefa '{task_id}': sem resposta do ClickUp ({type(e).__name__})")
        return None
    
# --------------------------------------------------------------------------------------------------------------------------------------------

# Obter tarefas - Objeto (Obter as "Tarefas Abertas" para o Dashboard)
def get_tasks(statuses: list | None = None, assignees: list | None = None) -> list | None:
    url = f"{BASE_URL}/list/{CLICKUP_LIST_ID}/task"
    params = {}
    if statuses:
        params["statuses[]"] = statuses
    if assignees:
        params["assignees[]"] = assignees
    try:
        response = session.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        tasks = response.json().get("tasks", [])
        logger.info(f"{len(tasks)} tarefas obtidas da List ID: '{CLICKUP_LIST_ID}'")
        return tasks
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            logger.error(f"Erro ao obter tarefas da List ID: '{CLICKUP_LIST_ID}': {e.response.status_code} - {e.response.text}")
        else:
            logger.error(f"Erro ao obter tarefas da List ID: '{CLICKUP_LIST_ID}': sem resposta do ClickUp ({type(e).__name__})")
        return None
        
# --------------------------------------------------------------------------------------------------------------------------------------------

# Status da Tarefa - Objeto
def is_task_completed(task_id: str) -> bool:
    task = get_task(task_id)
    if task is None:
        return False
    return task.get("status", {}).get("type", "") == "closed"
    