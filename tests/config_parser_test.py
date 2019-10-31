import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from src.config_parser import ConfigParser
from src.errors import MissingOptionError, OptionTypeError, OptionValueError

import pytest
import json



def test_correct_config(tmpdir):
    config = {'GP': -2, 'DIFF': -5, 'SAME': 5, 'MAX_NUMBER_PATHS': 3, 'MAX_SEQ_LENGTH': 10}
    path = tmpdir.join('config_tmp.txt')
    parser = ConfigParser()
    with open(path, 'w') as f:
        json.dump(config, f)

    loaded_config = parser.load_config(path)
    assert loaded_config == config


def test_not_json(tmpdir):
    config = 'not json'
    path = tmpdir.join('config_tmp.txt')
    parser = ConfigParser()
    with open(path, 'w') as f:
        f.write(config)
        
    with pytest.raises(json.JSONDecodeError):
        _ = parser.load_config(path)


def test_missing_options(tmpdir):
    config = {'GP': -2, 'DIFF': -5, 'MAX_NUMBER_PATHS': 3, 'MAX_SEQ_LENGTH': 10}
    path = tmpdir.join('config_tmp.txt')
    parser = ConfigParser()
    with open(path, 'w') as f:
        json.dump(config, f)

    with pytest.raises(MissingOptionError):
        _ = parser.load_config(path)


def test_wrong_type_options(tmpdir):
    config = {'GP': -2, 'DIFF': -5, 'SAME': 5, 'MAX_NUMBER_PATHS': 'not int', 'MAX_SEQ_LENGTH': 10}
    path = tmpdir.join('config_tmp.txt')
    parser = ConfigParser()
    with open(path, 'w') as f:
        json.dump(config, f)

    with pytest.raises(OptionTypeError):
        _ = parser.load_config(path)


def test_wrong_max_paths_value(tmpdir):
    config = {'GP': -2, 'DIFF': -5, 'SAME': 5, 'MAX_NUMBER_PATHS': -4, 'MAX_SEQ_LENGTH': 10}
    path = tmpdir.join('config_tmp.txt')
    parser = ConfigParser()
    with open(path, 'w') as f:
        json.dump(config, f)

    with pytest.raises(OptionValueError):
        _ = parser.load_config(path)


def test_wrong_max_seq_len_value(tmpdir):
    config = {'GP': -2, 'DIFF': -5, 'SAME': 5, 'MAX_NUMBER_PATHS': 10, 'MAX_SEQ_LENGTH': -4}
    path = tmpdir.join('config_tmp.txt')
    parser = ConfigParser()
    with open(path, 'w') as f:
        json.dump(config, f)

    with pytest.raises(OptionValueError):
        _ = parser.load_config(path)