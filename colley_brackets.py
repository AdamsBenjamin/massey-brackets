# !/usr/bin/env python3
# encoding: utf-8

import numpy as np
import json
import sys
import os

__author__ = 'Benjamin Adams'
__version__ = '0.1'
__email__ = 'adams.benjamin@protonmail.com'
__credit__ = 'Benjamin Adams, Jenna Schachner, Gabriel Mercer'


class ColleyBracket(object):
    data = None

    def __init__(self, filename):
        if not os.path.isfile(filename) or not filename.endswith('.json'):
            with open(filename, 'r') as fp:
                self.data = json.open(fp)
        _generate_matrices(self)

    def _generate_matrices(self):
        _num_teams = len(set([i['home']['team'] for i in self.data]))
        self.C = [[0 if row != col else 2 for row
                  in range(_num_teams)] for col in range(_num_teams)]
        self.b = [0]
        self._team_index = {}
        team_counter = 0

        for entry in self.data:
            if entry['home']['team'] not in self._team_index:
                self._team_index[entry['home']['team']] = team_counter
                team_counter += 1
            if entry['away']['team'] not in self._team_index:
                self._team_index[entry['away']['team']] = team_counter
                team_counter += 1

            home_index = self._team_index[entry['home']['team']]
            away_index = self._team_index[entry['away']['team']]
            self.C[home_index][home_index] += 1
            self.C[away_index][away_index] += 1
            self.C[home_index][away_index] -= 1
            self.C[away_index][home_index] -= 1

    def rank_teams(self):
        pass
