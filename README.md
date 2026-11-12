# Jornada Matte

O projeto é uma automação de onboarding pós-venda da Matte, rodando como função serverless (AWS Lambda via handler.py).

O fluxo é sequencial: cada stage cria uma tarefa (e subtarefas) no ClickUp para a equipe executar manualmente, e um "check" correspondente verifica periodicamente (via is_task_completed) se aquela tarefa foi concluída no ClickUp — quando concluída, ele dispara a criação do próximo stage e atualiza o registro do projeto no Supabase (current_stage).

---------------------------------------------------------------------------------------------------------------------------------------

# Para que serve

- O objetivo é padronizar a implementação de CRM e IA para todo cliente novo: em vez de depender da memória do time, a automação cria automaticamente as tarefas e subtarefas de cada etapa no ClickUp 

- Depois que o projeto é concluído, a automação também mantém o acompanhamento recorrente (validações semanais e checkpoints mensais), garantindo que nenhum cliente fique sem contato após a entrega.

---------------------------------------------------------------------------------------------------------------------------------------

## Como rodar
1. Clone o repositório
2. Copie `.env.example` para `.env` e preencha as variáveis
3. Instale as dependências: `pip install -r requirements.txt`
4. Rode: `python handler.py`

---------------------------------------------------------------------------------------------------------------------------------------

## Estrutura
- `stages/` — lógica de cada etapa do onboarding
- `core/` — banco de dados, logging, notificações
- `integrations/` — ClickUp
- `handler.py` — funções Lambda: `webhook` (disparo), `check_stages` (checagem periódica), `dashboard` (acompanhamento)

---------------------------------------------------------------------------------------------------------------------------------------

# Explicação por Stages

1. Disparo inicial: Roda quando os dados de um cliente novo é recebido
Boas-Vindas e Apresentação do Time

2. Acontece após o Onboarding, com tarefas para enviar instruções de assinar o CRM e pegar Feedback

3.

3A -> Personalizar CRM
3B -> Criação da IA
3C -> Revisão da IA
3D -> Entrega da IA

4.

4A -> Onboarding do CRM
4B -> Foi desativado

5. 

Validação(15 em 15 dias)
Checkpoint(30 em 30 dias)

---------------------------------------------------------------------------------------------------------------------------------------

# Como dar Deploy

## Windows (WSL)

- Abra o PowerShell modo admin
- Escreva: "wsl"
- Abrir pasta cd "/mnt/c/Personal/Programming/Python/Jornada Matte - Automação Python"
- Depois de "serverless deploy"

## Linux

```bash
cd ~/Pessoal/Code/Jornada-Matte
npx serverless deploy 
```
