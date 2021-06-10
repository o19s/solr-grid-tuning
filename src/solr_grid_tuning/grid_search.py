from itertools import chain, combinations, product
from sklearn.model_selection import ParameterGrid
from collections.abc import Iterable
from solr_grid_tuning.solr_query import SolrQuery

param_grid = {
    'qf': ['title', 'content', 'brandModelTokenized'],
    'pf': ['title', 'content', 'brandModelTokenized'],
    'field_weights': (0.0, 0.5, 0.75, 1.0),
    'tie': (0.0, 0.1, 0.2, 0.8),
    'mandatory': ['qf'],
    'optional': ['pf', 'tie']
}


def list_field_weight_combinations(query_param: str):
    field_weights = list(product(range(len(param_grid['field_weights'])), repeat=len(param_grid[query_param])))
    all_weights = []
    for fw in field_weights:  # (0, 1, 2)
        individual_weight_params = {}
        for i, weight in enumerate(fw):
            if weight == 0:
                continue
            else:
                individual_weight_params[param_grid[query_param][i]] = param_grid['field_weights'][weight]

        # we don't want an empty dictionary of weights for mandatory query parameters
        if query_param in param_grid['mandatory'] and len(individual_weight_params) == 0:
            pass
        else:
            param_string = []
            for k, v in individual_weight_params.items():
                param_string.append(f'{k}^{v}')

            all_weights.append(' '.join(param_string))
    return all_weights


def get_param_grid():
    params = {
        'qf': list_field_weight_combinations('qf'),
        'pf': list_field_weight_combinations('pf'),
        'tie': param_grid['tie']
    }
    return ParameterGrid(params)


def create_query_params_from_grid(params):
    fl = params['fl']
    if 'pf' in params:
        pass
    if 'tie' in params:
        pass
    for k, v in params:
        print(k, v)
    return 'query'


if __name__ == '__main__':
    pg = list(get_param_grid())
    print(f'Total parameter combinations to try: {len(pg)}')
