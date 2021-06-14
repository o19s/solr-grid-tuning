import math
import pandas as pd

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# document id -> judgement for that document
JudgedDocuments = Dict[str, float]


@dataclass
class JudgedQuery:
    query: str
    judgements: JudgedDocuments

    def __post_init__(self):
        self.documents_in_ideal_order: List[Tuple[str, float]] = sorted(self.judgements.items(),
                                                                        key=lambda item: item[1], reverse=True)

    def get_judgement(self, doc_id: str) -> Optional[float]:
        return self.judgements.get(doc_id)

    def idcg(self, at_n: int = 10):
        idcg = 0
        for i in range(min(len(self.documents_in_ideal_order), at_n)):
            denom = math.log(i + 2, 2)
            idcg += self.documents_in_ideal_order[i][1] / denom
        return idcg


def read_judgements_file(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=0, dtype={'query': str, 'docid': str, 'rating': float})
    return df


def read_judgements_to_dict(filename: str) -> Dict[str, JudgedQuery]:
    df = read_judgements_file(filename)
    judgements: Dict[str, JudgedQuery] = {}
    for row in df.itertuples():
        judged_query = judgements.get(row.query, JudgedQuery(row.query, {}))
        if not math.isnan(row.rating):
            judged_query.judgements.update({row.docid: row.rating})
            judgements.update({row.query: judged_query})
        judged_query.__post_init__()
    return judgements


class Judgements:

    def __init__(self, judgements_file: str):
        self.judged_queries: Dict[str, JudgedQuery] = read_judgements_to_dict(judgements_file)

    def get_judgements_for_query(self, query: str) -> Optional[JudgedQuery]:
        return self.judged_queries.get(query)

    def get_judgement(self, query: str, doc: str) -> Optional[float]:
        return self.get_judgements_for_query(query).get_judgement(doc)
