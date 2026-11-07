import json
import time
import traceback

from core.helpers import notify_acompanhamento
from core.logger import get_logger
from stages.stage_1.stage_1 import run

logger = get_logger(__name__)

headers = {
    "Acess-Control-Allow-Origin": "*",
    "Acess-Control-Allow-Headers": "Content-Type"
}

#  --------------------------------------------------------------------------

# Webhook
def webhook(event: dict, context: object) -> dict:

    try:
        body: dict = json.loads(event.get("body", "{}"))

        client_name: str = body["client_name"]
        company_name: str = body["company_name"]

        run(client_name, company_name)

        notify_acompanhamento(
            f"🛠️Projeto da empresa {company_name} foi iniciado.",
            f"Nome do cliente: {client_name}",
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"Ok": True}),
        }

    except Exception as e:
        logger.error(f"Erro: {type(e).__name__}: {e}")
        logger.error(traceback.format_exc())
        # logger.error(f"Webhook com erro: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"Error": str(e)}),
        }

#  --------------------------------------------------------------------------

MAX_TENTATIVAS = 3

# Verifica as tarefas concluídas
def check_stages(event: dict, context: object) -> dict:

    from stages.stage_1.stage_1_check import check_stage_1
    from stages.stage_2.stage_2_check import check_stage_2
    from stages.stage_3.stage_3_a.stage_3a_check import check_stage_3a
    from stages.stage_3.stage_3_b.stage_3b_check import check_stage_3b
    from stages.stage_3.stage_3_c.stage_3c_check import check_stage_3c
    from stages.stage_3.stage_3_d.stage_3d_check import check_stage_3d
    from stages.stage_4.stage_4_check import check_stage_4a

    for nome, func in [
        ("stage_1", check_stage_1),
        ("stage_2", check_stage_2),
        ("stage_3.stage_3_a", check_stage_3a),
        ("stage_3.stage_3_b", check_stage_3b),
        ("stage_3.stage_3_c", check_stage_3c),
        ("stage_3.stage_3_d", check_stage_3d),
        ("stage_4", check_stage_4a),
    ]:
        for tentativa in range(1, MAX_TENTATIVAS + 1):

            try:
                func()
                break
            except Exception as e:
                logger.error(f"Erro no {nome} (tentativa {tentativa} de {MAX_TENTATIVAS})")

                if tentativa == MAX_TENTATIVAS:
                    logger.error(f"Erro na verificação da tarefa: {type(e).__name__}: {e}")
                    logger.error(traceback.format_exc())
                    break
                
                else:
                    time.sleep(3)

    return {"statusCode": 200, "body": json.dumps({"Ok": True})}

