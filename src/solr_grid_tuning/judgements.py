from typing import Dict
import pandas as pd


def read_judgements_file(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=0, dtype={'query': str, 'docid': str, 'rating': float})
    return df


class Judgements:

    def __init__(self, judgements_file: str):
        self.judgements_file = judgements_file
        self.judgements = read_judgements_file(judgements_file)
        self.judgement_groups = self.judgements.groupby('query').groups

    def get_judgements_for_query(self, query: str) -> pd.ndarray:
        return self.judgement_groups['query']
