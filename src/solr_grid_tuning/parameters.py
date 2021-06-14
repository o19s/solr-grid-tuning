from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import itertools
import json


def load_parameter_config(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return ParameterConfig.from_dict(data)


def weights_parameters(fields: List[str], weights: List[float]) -> List[str]:
    """Generate Solr field weight combinations for given field values and weights
    e.g. for ["content", "title"] and [0.1, 1.0] it generates
    ["content^0.1 title^0.1", "content^0.1 title^1.0", "content^1.0 title0.1", "content^1.0 title^1.0"]
    """
    fields_and_weights: List[List[str]] = [[f"{field}^{weight}" for weight in weights] for field in fields]
    return [" ".join(combination) for combination in itertools.product(*fields_and_weights)]


@dataclass
class ParameterConfig:
    # the parameter space with a tuple for each parameter key and its values
    parameters: List[Tuple[str, List[str]]]

    def all_combinations(self):
        parameters_with_values = [itertools.product([param], values) for param, values in self.parameters]

        # multiply them to get all parameter combinations, i.e. the "grid"
        return list(itertools.product(*parameters_with_values))

    @staticmethod
    def from_dict(config: Dict[str, Any]):
        parameters: List[Tuple[str, List[str]]] = []
        for param, values in config.items():
            if param == 'qf' or param == 'pf':
                # special handling of qf/pf, parameters are specified as combinatios of field+weight in a dict
                weights = weights_parameters(values['fields'], values['weights'])
                parameters.append((param, weights))
            else:
                parameters.append((param, values))
        return ParameterConfig(parameters)
