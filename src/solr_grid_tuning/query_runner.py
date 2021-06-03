from typing import List, Tuple

from solr_grid_tuning.solr_client import SolrClient
from solr_grid_tuning.solr_query import SolrQuery


class QueryRunner:

    def run_searches_with_parameters(self, client: SolrClient, base_query: SolrQuery, searches: List[str], return_field="id"):
        """Performs queries for each of the given search terms by successively setting them on a base query
        """
        results = []
        for search in searches:
            query = dataclasses.replace(base_query, q=search)
            result = self.run_query(client, query, return_field)
            results.append((search, result))
        return results


    def run_queries(self, client: SolrClient, queries: List[SolrQuery], return_field="id") -> List[Tuple[str, List[str]]]:
        """Runs queries with the given parameter and returns a list of return_field values.
        """
        results = []
        for query in queries:
            result = self.run_query(client, query, return_field)
            results.append((query, result))
        return results

    def run_query(self, client: SolrClient, query: SolrQuery, return_field="id") -> List[str]:
        response = client.query(query)
        if response["docs"] is not None and len(response["docs"]) > 0:
            return [doc[return_field] for doc in response["docs"]]
        else:
            return []
