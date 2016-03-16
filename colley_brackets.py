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
    def __init__(self, filename):
        if not os.path.isfile(filename) or not filename.endswith('.json'):
            with open(filename, 'r') as fp:
                self.data = json.open(fp)
        _generate_matrices()

    def _generate_matrices(self):
        # Count the teams.
        _num_teams = len(set([i['home']['team'] for i in self.data]))

        # Create square array, C, of length _num_teams.
        # The diagonal will be 2s; the rest will be filled with 0s.
        self.C = [[
            (0 if row != col else 2)
            for in range(_num_teams)]
            for col in range(_num_teams)]

        # Create array for storing game outcomes.
        # Results are cumulative.
        wins = [0] for _ in range(_num_teams)

        # Dictionary for storing team names and
        # their associated team id numbers.
        self._team_index = {}
        team_counter = 0

        for entry in self.data:
            # Guarantee that each team has a unique id number.
            if entry['home']['team'] not in self._team_index:
                self._team_index[entry['home']['team']] = team_counter
                team_counter += 1
            if entry['away']['team'] not in self._team_index:
                self._team_index[entry['away']['team']] = team_counter
                team_counter += 1

            home_index = self._team_index[entry['home']['team']]
            away_index = self._team_index[entry['away']['team']]
            # Alter C to represent the game's happening.
            self.C[home_index][home_index] += 1
            self.C[away_index][away_index] += 1
            self.C[home_index][away_index] -= 1
            self.C[away_index][home_index] -= 1

            # Alter the cumulative wins for each team
            # depending on the game's outcome.
            if entry['home']['pts'] > entry['away']['pts']:
                wins[home_index] += 1
                wins[away_index] -= 1
            else:
                wins[away_index] += 1
                wins[home_index] -= 1

        # Uses the wins array to produce the b array
        # needed by the Colley method.
        self.b = map(lambda i: 1 + (float(i) / 2), wins)

    def rank_teams(self):
        # TODO: Finish function for ranking teams.
        pass
