from solr_grid_tuning.parameters import ParameterConfig


def test_parameter_simple():
    config = ParameterConfig.from_dict({'paramA': [1, 2], 'paramB': [3, 4]})
    assert (config.all_combinations() == [
        (('paramA', 1), ('paramB', 3)),
        (('paramA', 1), ('paramB', 4)),
        (('paramA', 2), ('paramB', 3)),
        (('paramA', 2), ('paramB', 4)),
    ])


def test_parameter_with_qf():
    config = ParameterConfig.from_dict({'qf': {'fields': ['field1', 'field2'], 'weights': [0.5, 5]}, 'tie': [0.5, 1]})
    assert (config.all_combinations() == [
        (('qf', 'field1^0.5 field2^0.5'), ('tie', 0.5)),
        (('qf', 'field1^0.5 field2^0.5'), ('tie', 1)),
        (('qf', 'field1^0.5 field2^5'), ('tie', 0.5)),
        (('qf', 'field1^0.5 field2^5'), ('tie', 1)),
        (('qf', 'field1^5 field2^0.5'), ('tie', 0.5)),
        (('qf', 'field1^5 field2^0.5'), ('tie', 1)),
        (('qf', 'field1^5 field2^5'), ('tie', 0.5)),
        (('qf', 'field1^5 field2^5'), ('tie', 1)),
    ])
