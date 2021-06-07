from functools import lru_cache
from typing import Dict
import pandas as pd


def read_judgements_file(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=0, dtype={'query': str, 'docid': str, 'rating': float})
    return df


class Judgements:

    def __init__(self, judgements_file: str):
        self.judgements_file = judgements_file
        self.judgements: pd.DataFrame = read_judgements_file(judgements_file)
        self.judgement_groups: pd.DataFrameGroupBy = self.judgements.groupby('query')

    @lru_cache(maxsize=100)
    def get_judgements_for_query(self, query: str) -> Dict[str, float]:
        return self.judgement_groups.get_group(query)\
            .drop(columns='query').set_index('docid')\
            .to_dict().get('rating')

    @lru_cache(maxsize=1_000)
    def get_judgement(self, query: str, doc: str) -> float:
        return self.get_judgements_for_query(query).get(doc)
