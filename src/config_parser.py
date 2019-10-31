from .errors import MissingOptionError, OptionTypeError, OptionValueError

import sys
import json
import logging
import numpy as np


class ConfigParser:
    def __init__(self):
        self.required_opts = ['SAME', 'DIFF', 'GP', 'MAX_NUMBER_PATHS', 'MAX_SEQ_LENGTH']
        self.opt_types = [int, int, int, int, int]
        self.opt_constraints = [[('', 0)], [('', 0)], [('', 0)], [('>', 0)], [('>', 0)]]
        self.constraint_functions = {
            '':       (lambda val, border: True, 
                       lambda opt, val, border: ''),
            '<=':     (lambda val, border: val <= border, 
                       lambda opt, val, border: f'{opt} = {val}, but should be <= {border}'), 
            '>=':     (lambda val, border: val >= border, 
                       lambda opt, val, border: f'{opt} = {val}, but should be >= {border}'),
            '==':     (lambda val, border: val == border, 
                       lambda opt, val, border: f'{opt} = {val}, but should be == {border}'),
            '!=':     (lambda val, border: val != border, 
                       lambda opt, val, border: f'{opt} = {val}, but should be != {border}'),
            '>':      (lambda val, border: val > border, 
                       lambda opt, val, border: f'{opt} = {val}, but should be > {border}'),
            '<':      (lambda val, border: val < border, 
                       lambda opt, val, border: f'{opt} = {val}, but should be < {border}'),
            'in':     (lambda val, border: val >= border[0] and val <= border[1], 
                       lambda opt, val, border: f'{opt} = {val}, but should be in {border}'),
            'not in': (lambda val, border: val < border[0] or val > border[1], 
                       lambda opt, val, border: f'{opt} = {val}, but should be outside {border}')
        }

    def load_config(self, path):
        config = self.load_json(path)
        self._check_options(config)
        return config

    def _check_options(self, config):
        self._check_if_all_present(config)
        self._check_values(config)

    def _check_if_all_present(self, config):
        opt_present = np.array([opt in config for opt in self.required_opts])
        if not all(opt_present):
            missing = np.array(self.required_opts)[~opt_present]
            raise MissingOptionError(f'Missing config options: {missing}')

    def _check_values(self, config):
        for opt, type_, constraints in zip(self.required_opts, self.opt_types, self.opt_constraints):
            self._check_value(opt, config[opt], type_, constraints)

    def _check_value(self, opt, value, type_, constraints):
        if not isinstance(value, type_):
            raise OptionTypeError(f'{opt} is type {type(value).__name__}, but should be type {type_.__name__}')

        for condition, border in constraints:
            if not self.constraint_functions[condition][0](value, border):
                raise OptionValueError(self.constraint_functions[condition][1](opt, value, border))

    
    def load_json(self, path):
        with open(path) as f:
            config = json.load(f)
        return config
