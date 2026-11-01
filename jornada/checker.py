from constants import Etapas
from core.helpers import checker, checker_duo, checker_final
from jornada.etapa_2.ui_ux import create_stage_2
from jornada.etapa_3.criar import create_stage_3b
from jornada.etapa_3.personalizar import create_stage_3a
from jornada.etapa_4.revisao import create_stage_3c
from jornada.etapa_4.visao_geral import create_stage_4a
from jornada.etapa_5.entrega import create_stage_3d


def run_all_checks() -> None:
    checker(Etapas.ETAPA_1, Etapas.ETAPA_2, create_stage_2)

    checker_duo(
        Etapas.ETAPA_2,
        (Etapas.ETAPA_3_PERSONALIZAR, create_stage_3a),
        (Etapas.ETAPA_3_CRIAR, create_stage_3b),
    )

    checker(Etapas.ETAPA_3_PERSONALIZAR, Etapas.ETAPA_4_VISAO_GERAL, create_stage_4a)
    checker(Etapas.ETAPA_3_CRIAR, Etapas.ETAPA_4_REVISAO, create_stage_3c)
    checker(Etapas.ETAPA_4_REVISAO, Etapas.ETAPA_5, create_stage_3d)

    checker_final(Etapas.ETAPA_5, Etapas.ETAPA_5)

