from solr_grid_tuning.solr_client import SolrClient
from solr_grid_tuning.solr_query import SolrQuery
from solr_grid_tuning.query_runner import QueryRunner

# This is the configuration of the local Solr instance that is assumed by this test
base_url = "http://localhost:8983/solr"
collection = "tmdb"
request_handler = "select"


def test_basic_query():
    solr_client = SolrClient(base_url, auth=None, collection=collection, request_handler=request_handler)
    solr_query = SolrQuery(q="star wars", fl=["id"], other_params=[("qf", "title")])
    query_runner = QueryRunner()
    results = query_runner.run_query(solr_client, solr_query)
    assert len(results) == 10
