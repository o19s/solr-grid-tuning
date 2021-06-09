import os

from solr_grid_tuning.metrics_calculation import ndcg
from solr_grid_tuning.judgements import read_judgements_file


def test_optimal_list():
    judgements = {'a': 1, 'b': 0, 'c': 0, 'd': 1}
    document_ids = ['a', 'd', 'c', 'b']
    assert ndcg(judgements, document_ids) == 1


def test_non_optimal_list():
    judgements = {'a': 1, 'b': 0, 'c': 0, 'd': 1}
    document_ids = ['b', 'a', 'd', 'c']
    # DCG = 0 + 1/1.58496250072 + 1/2 + 0 = 1.13
    # IDCG = 1/1 + 1/1.58496250072 + 0 + 0 = 1.63
    assert round(ndcg(judgements, document_ids), 2) == 0.69


def test_average_is_taken_for_unrated_documents():
    judgements = {'a': 1, 'b': 0, 'c': 0, 'd': 1}
    document_ids = ['e', 'b', 'a']
    # DCG = 0.5/1 + 0/1.58496250072 + 1/2 = 1
    # IDCG = 1/1 + 1/1.58496250072 + 0 + 0 = 1.63
    assert round(ndcg(judgements, document_ids), 2) == 0.61


def test_judgements_file():
    this_dir = os.path.dirname(__file__)
    example_file = os.path.join(this_dir, '../example/Judgement_Catalog_basic.csv')
    df = read_judgements_file(example_file)
    assert (df.columns.array == ['query', 'docid', 'rating'])


# calculate ndcg for 'tienda remolque'


if __name__ == '__main__':
    test_judgements_file()
