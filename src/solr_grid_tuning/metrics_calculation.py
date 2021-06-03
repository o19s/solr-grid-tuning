from typing import List, Dict, Tuple

import math


def ndcg(judgements: Dict[str, float], document_ids: List[str], at_n=10) -> float:
    # todo: handle unrated documents, use a reasonable default, average?
    documents_scored: List[Tuple[str, float]] = [(id, judgements.get(id, 0.5)) for id in document_ids]
    judgements_sorted: List[Tuple[str, float]] = sorted(judgements.items(), key=lambda item: item[1], reverse=True)
    return _ndcg(judgements_sorted, documents_scored)


def _ndcg(judged_items_sorted: List[Tuple[str, float]], list_sorted: List[Tuple[str, float]], at_n=10) -> float:
    judged_scores: List[float] = [item_and_score[1] for item_and_score in judged_items_sorted]
    list_scores: List[float] = [item_and_score[1] for item_and_score in list_sorted]

    dcg = 0
    idcg = 0
    for i in range(min(len(judged_scores), len(list_scores), at_n)):
        denom = math.log(i + 2, 2)
        dcg += list_scores[i] / denom
        idcg += judged_scores[i] / denom
    if idcg > 0:
        ndcg = min(dcg, idcg) / idcg
    else:
        ndcg = None
    return ndcg
