import json
from argparse import ArgumentParser
from typing import Any, Dict

from solr_grid_tuning.judgements import Judgements
from solr_grid_tuning.parameters import ParameterConfig
from solr_grid_tuning.query_runner import QueryRunner
from solr_grid_tuning.solr_client import SolrClient
from solr_grid_tuning.solr_query import SolrQuery


def load_config(config) -> Dict[str, Any]:
    with open(config) as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("config", help="configuration file")
    args = parser.parse_args()

    config = load_config(args.config)

    solr_client = SolrClient(base_url=config['solr']['url'], collection=config['solr'].get('collection'),
                             request_handler=config['solr'].get('request_handler'))
    query_runner = QueryRunner(solr_client, query_field=config['solr']['query_field'],
                               document_id_field=config['solr']['document_id_field'])
    solr_base_query = SolrQuery.from_dict(config['base_parameters'])
    parameter_config = ParameterConfig.from_dict(config['grid_parameters'])
    rated_queries = [judged_query.query for judged_query in Judgements(config['judgements']).judged_queries.values()]

    query_runner.run(solr_base_query, rated_queries, parameter_config.all_combinations(), 'results.tsv')
