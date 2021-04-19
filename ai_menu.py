import common as cm
from ais.ai_greedy import ai_greedy as AI_1
from ais.ai_search import ai_search as AI_2
from ais.ai_search import ai_search_q as AI_3
from ais.ai_search import ai_search_calc as AI_4
from ais.ai_base import ai_base as AI_0
from ais.ai_mtcl import ai_mtcl as AI_5

def get_AI(id):
    ret = globals()['AI_'+str(id)](cm.GB_size)
    return ret