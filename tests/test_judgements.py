import os
from solr_grid_tuning.judgements import Judgements


JUDGE_CSV = '../example/Judgement_Catalog_basic.csv'
QUERY = 'warhammer'
DOC_ID = '639240626'

this_dir = os.path.dirname(__file__)
example_file = os.path.join(this_dir, JUDGE_CSV)


def test_init():
    judgements = Judgements(example_file)
    assert(judgements.judgement_groups.ngroups > 1)

    jfc = judgements.get_judgements_for_query(query=QUERY)
    assert(len(jfc) == 11)

    rating = judgements.get_judgement(query=QUERY, doc=DOC_ID)
    assert(rating == 2.0)


if __name__ == '__main__':
    test_init()
