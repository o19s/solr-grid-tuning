from solr_grid_tuning.metrics_calculation import ndcg


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
