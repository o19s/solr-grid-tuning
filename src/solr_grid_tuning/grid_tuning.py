import dataclasses
import itertools
from typing import Any, List, Dict, Optional, Tuple

import metrics_calculation
from solr_grid_tuning.judgements import JudgedQuery
from solr_grid_tuning.query_runner import QueryRunner
from solr_grid_tuning.solr_query import SolrQuery


# Generate Solr field weight combinations for given field values and weights
# e.g. for ["content", "title"] and [0.1, 1.0] it generates
#   ["content^0.1 title^0.1", "content^0.1 title^1.0", "content^1.0 title0.1", "content^1.0 title^1.0"]
def weights_parameters(fields: List[str], weights: List[float]) -> List[str]:
    fields_and_weights: List[List[str]] = [[f"{field}^{weight}" for weight in weights] for field in fields]
    return [" ".join(combination) for combination in itertools.product(*fields_and_weights)]


class SolrGridTuning:

    def __init__(self, query_runner: QueryRunner):
        self.query_runner = query_runner

    def parameter_ndcgs(self,
                        base_solr_query: SolrQuery,
                        judged_queries: List[JudgedQuery],
                        parameter_values: Dict[str, List[Any]],
                        query_field="q",
                        document_id_field="id"):
        parameters_with_values = [itertools.product([param], values) for param, values in parameter_values.items()]

        # multiply them to get all parameter combinations, i.e. the "grid"
        parameter_grid = list(itertools.product(*parameters_with_values))

        print(f"Trying {len(judged_queries)} queries with {len(parameter_grid)} parameters")

        parameter_ndcgs = []
        for parameter_combination in parameter_grid:
            ndcg = self.ndcg_for_parameter_combination(base_solr_query, judged_queries, list(parameter_combination),
                                                       query_field, document_id_field)
            if ndcg is not None:
                parameter_ndcgs.append((parameter_combination, ndcg))
            else:
                print(
                    f"No NDCG calculated for combination {parameter_combination}, probably judgements did not cover the result.")
        return parameter_ndcgs

    def ndcg_for_parameter_combination(self,
                                       base_query: SolrQuery,
                                       judged_queries: List[JudgedQuery],
                                       parameter_combination: List[Tuple[str, Any]],
                                       query_field='q',
                                       document_id_field='id') -> Optional[float]:
        ndcgs = []
        for judged_query in judged_queries:
            # set the actual search term
            query = dataclasses.replace(base_query, q=judged_query.query) if query_field == 'q' else base_query
            search_as_custom_parameter = [(query_field, judged_query.query)] if query_field != 'q' else []

            # set the current parameter combination
            query.other_params = (query.other_params if query.other_params is not None else []) + search_as_custom_parameter + parameter_combination

            # run the query
            result_ids = self.query_runner.run_query(query, return_field=document_id_field)
            ndcg = metrics_calculation.ndcg(judged_query.judgements, result_ids)
            if ndcg is not None:
                ndcgs.append(ndcg)
            else:
                print(f"No NDCG calculated for {judged_query.query} and {parameter_combination}")
        return sum(ndcgs) / len(ndcgs) if len(ndcgs) > 0 else None
