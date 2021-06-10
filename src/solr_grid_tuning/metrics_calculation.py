from typing import List, Dict, Optional, Tuple

import math

MIN_RATED_PCT = 50


# Based on the given judgements score the ordered list of document IDs in document_ids
def ndcg(judgements: Dict[str, float], document_ids: List[str], at_n=10) -> Optional[float]:
    judgements_sorted: List[Tuple[str, float]] = sorted(judgements.items(), key=lambda item: item[1], reverse=True)

    # For each document on the list, get its judgment (which may be None if the document has not been judged so far)
    scored_docs: List[Tuple[str, Optional[float]]] = [(d_id, judgements.get(d_id)) for d_id in document_ids][:at_n]
    if len(scored_docs) == 0:
        return None

    # only calculate the ndcg for lists that have at least MIN_RATED_PCT percent of documents rated
    documents_with_score = [d for d in scored_docs if d[1] is not None]
    rated_pct = 100 * len(documents_with_score) / len(scored_docs)

    if rated_pct >= MIN_RATED_PCT:
        rating_average = sum([d[1] for d in documents_with_score]) / len(documents_with_score)
        # fill the unrated documents with the average, this likely over-rates them but that's fine for now
        scored_docs_adjusted = [d if d[1] is not None else (d[0], rating_average) for d in scored_docs]
        return _ndcg(judgements_sorted, scored_docs_adjusted, at_n)
    else:
        return None


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
