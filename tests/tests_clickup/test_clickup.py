import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from integrations.clickup import create_task, create_subtask

# Criar uma Tarefa
task = create_task(
    name="[TESTE] Abertura do Projeto",
    description="Tarefa de teste — pode apagar",
    markdown_content="## Tarefa de teste\n\npode apagar",
    assignees=[],
    due_date=None
)

if task:
    # Criar Sub-tarefa
    create_subtask(
        parent_task_id=task["id"],
        name="[TESTE] Sub-tarefa de exemplo",
        description="Sub-tarefa de teste — pode apagar",
        markdown_content="## Sub-tarefa de teste\n\npode apagar",
        assignees=[],
        due_date=None
    )