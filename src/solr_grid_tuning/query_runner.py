import dataclasses
from typing import Any, List, Tuple

from solr_grid_tuning.solr_client import SolrClient
from solr_grid_tuning.solr_query import SolrQuery


class QueryRunner:

    def __init__(self, solr_client: SolrClient, query_field: str = 'q', document_id_field: str = 'id'):
        self.solr_client = solr_client
        self.query_field = query_field
        self.document_id_field = document_id_field

    def run(self,
            base_query: SolrQuery,
            searches: List[str],
            parameter_combinations: List[List[Tuple[str, Any]]],
            output_file: str):

        print(
            f"Running {len(searches)} searches with {len(parameter_combinations)} parameter combinations = {len(searches) * len(parameter_combinations)} queries.")

        with open(output_file, "w") as output:
            # header contains all parameter columns and a column for the query and the document ids
            parameter_columns = set([f'param_{key}' for parameter_combination in parameter_combinations for (key, _) in
                                     parameter_combination])
            columns = list(parameter_columns) + [self.query_field, 'documents']
            output.write('\t'.join(sorted(columns)) + "\n")

            # for each parameter combination: run it, store results in TSV
            for parameter_combination in parameter_combinations:
                params_dict = dict([(f'param_{key}', str(value)) for (key, value) in parameter_combination])
                results = self.run_searches_with_parameters(base_query, searches, parameter_combination)
                for (search, result) in results:
                    results_dict = {self.query_field: search, 'documents': ','.join(result)}
                    row_as_dict = sorted(dict(**params_dict, **results_dict).items())
                    row = '\t'.join([value[1] for value in row_as_dict])
                    output.write(row + "\n")

    def run_searches_with_parameters(self,
                                     base_query: SolrQuery,
                                     searches: List[str],
                                     parameter_combination: List[Tuple[str, Any]]) -> List[Tuple[str, List[str]]]:
        """Performs queries for each of the given searches for the given parameter combination
        """

        # join the existing params on the base query with the given parameter combination
        query_params = (base_query.other_params if base_query.other_params is not None else []) + list(
            parameter_combination)
        query_with_parameters = dataclasses.replace(base_query, other_params=query_params)
        return self.run_searches(query_with_parameters, searches)

    def run_searches(self,
                     base_query: SolrQuery,
                     searches: List[str]) -> List[Tuple[str, List[str]]]:
        """Performs queries for each of the given searches by successively setting them on a base query
        """

        results = []
        for search in searches:
            # set the actual search term, handle special case of the query parameter not being 'q'
            if self.query_field == 'q':
                query = dataclasses.replace(base_query, q=search)
            else:
                query_as_special_parameter = (self.query_field, search)
                query_params = (base_query.other_params if base_query.other_params is not None else []) + [
                    query_as_special_parameter]
                query = dataclasses.replace(base_query, other_params=query_params)

            # run the query
            result_ids = self.run_query(query, return_field=self.document_id_field)
            results.append((search, result_ids))
        return results

    def run_query(self, query: SolrQuery, return_field="id") -> List[str]:
        """Run a single query and return the list of document ids
        """

        print(f"Running request: {str(query)}")
        response = self.solr_client.query(query)
        if response["docs"] is not None and len(response["docs"]) > 0:
            return [doc[return_field] for doc in response["docs"]]
        else:
            return []
