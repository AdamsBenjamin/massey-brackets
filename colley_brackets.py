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
    """
    Provides the utilities needed to rank teams by utilizing the Colley method.
    Requires a .json file of game information to function properly.
    """
    def __init__(self, filename):
        self.data = 0
        if os.path.isfile(filename) and filename.endswith('.json'):
            with open(filename, 'r') as fp:
                self.data = json.load(fp)

    def generate_matrices(self):
        """Uses the provided .json file to construct the C and b arrays."""
        # Count the teams.
        num_teams = len(set([i['away']['team'] for i in self.data]))

        # Create square array, C, of length _num_teams.
        # The diagonal will be 2s; the rest will be filled with 0s.
        self.C = [[
            (0 if row != col else 2)
            for row in range(num_teams)]
            for col in range(num_teams)]

        # Create array for storing game outcomes.
        # Results are cumulative.
        wins = [0] * num_teams

        # Dictionary for storing team names and
        # their associated team id numbers.
        self.team_index = {}
        team_counter = 0

        for entry in self.data:
            # Guarantee that each team has a unique id number.
            if entry['home']['team'] not in self.team_index:
                self.team_index[entry['home']['team']] = team_counter
                team_counter += 1
            if entry['away']['team'] not in self.team_index:
                self.team_index[entry['away']['team']] = team_counter
                team_counter += 1

            home_index = self.team_index[entry['home']['team']]
            away_index = self.team_index[entry['away']['team']]
            # Alter C to represent the game's happening.
            self.C[home_index][home_index] += 1
            self.C[away_index][away_index] += 1
            self.C[away_index][home_index] -= 1
            self.C[home_index][away_index] -= 1

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

        self.C = np.array(self.C)
        self.b = np.array(self.b)

    def rank_teams(self):
        """
        Solves for the unfilled r matrix then constructs and sorts
        an array of tuples containing all team names and
        their associated ranks.
        """
        self. r = np.linalg.lstsq(self.C, self.b)[0]
        teams = [None] * len(self.team_index)
        for i in self.team_index.keys():
            teams[self.team_index[i]] = i
        self.ranks = zip(teams, self.r)
        self.ranks = list(reversed(sorted(self.ranks, key=lambda i: i[-1])))

    def display_rankings(self):
        """Prints the sorted list of team rankings to the console."""
        for i in range(len(self.ranks)):
            print(
                '{:3} {:40} {:.2f}'.format(
                    i+1, self.ranks[i][0], self.ranks[i][1]))

b = ColleyBracket('./2014.json')
b.generate_matrices()
b.rank_teams()
b.display_rankings()
