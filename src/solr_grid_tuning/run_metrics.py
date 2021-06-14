from argparse import ArgumentParser

import pandas as pd

from metrics_calculation import ndcg
from solr_grid_tuning.judgements import Judgements

"""Takes a judgements file and a query results file and appends the IDCG/NDCG as columns 
"""
if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("judgements", help="judgements CSV")
    parser.add_argument("results", help="query results TSV")
    parser.add_argument("output", help="query results TSV with judgements added")
    args = parser.parse_args()

    judgements = Judgements(args.judgements)
    df = pd.read_csv(args.results, delimiter='\t')

    def calculate_idcg(row):
        query = row['keywords']
        return judgements.get_judgements_for_query(query).idcg(at_n=10)

    def calculate_ndcg(row):
        query = row['keywords']
        documents = row['documents'].split(',')
        return ndcg(judgements.get_judgements_for_query(query).judgements, documents)

    df['idcg'] = df.apply(lambda row: calculate_idcg(row), axis=1)
    df['ndcg'] = df.apply(lambda row: calculate_ndcg(row), axis=1)
    df.to_csv(args.output, sep='\t')

    # Best NDCG calculation
    param_columns = [col for col in df.columns.values.tolist() if col.startswith("param_")]
    df['combined_params'] = df[param_columns].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
    best_ndcg = df.groupby('combined_params').agg({'ndcg': 'sum'}).sort_values("ndcg", ascending=False)
    print(best_ndcg)





