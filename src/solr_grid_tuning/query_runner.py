from typing import List, Tuple

from solr_grid_tuning.solr_client import SolrClient
from solr_grid_tuning.solr_query import SolrQuery


class QueryRunner:

    def run_queries(self, client: SolrClient, queries: List[SolrQuery], return_field="id") -> List[Tuple[str, List[str]]]:
        """Runs queries with the given parameter and returns a list of return_field values.
        :param client: the SolrClient
        :param queries: the queries
        :param return_field: the field values to gather and export, field values are always returned as string
        :return: a list of tuples consisting of the query and the list of the results return_field values
        """
        results = []
        for query in queries:
            response = client.query(query)
            if response["docs"] is not None and len(response["docs"]) > 0:
                result_values = [doc[return_field] for doc in response["docs"]]
                results.append((query, result_values))
        return results
