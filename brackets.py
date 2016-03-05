# !/usr/bin/env python
# encoding: utf-8

import numpy as np
import json
import os
import sys

__author__ = 'Benjamin Adams'
__version__ = '1.0'
__email__ = 'adamsbt@appstate.edu'
__credit__ = 'Benjamin Adams, Jenna Schachner, Gabriel Mercer'

def parse_stats(filename):
    # checks that the given file exists and is a valid format.
    if not os.path.isfile(filename) or not filename.endswith('.json'):
        sys.exit('Invalid path or file type.')

    # parses and saves the file data to an array.
    data = []
    with open(filename, 'r') as fp:
        data = json.load(fp)

    # returns the array of dictionaries parsed from the json file
    return data


def generate_matrices(data):
    num_teams = len(set([entry['home']['team'] for entry in data]))
    team_counter = 0
    home_benefit = 0
    M = []
    y = []
    team_index = {}

    # single-pass through all dictionaries in data array
    for entry in data:
        # checks that both teams have been assigned column numbers.
        # those that have not are assigned the next largest number.
        if entry['home']['team'] not in team_index:
            team_index[entry['home']['team']] = team_counter
            team_counter += 1
        if entry['away']['team'] not in team_index:
            team_index[entry['away']['team']] = team_counter
            team_counter += 1

        # sets the home and away team flags for the most recently
        # indexed game.
        M.append([0] * num_teams)

        M[-1][team_index[entry['home']['team']]] = 1
        M[-1][team_index[entry['away']['team']]] = -1

        # adds the newest game's point difference, in terms of the
        # home team, to the end of the y vector.
        y.append(entry['home']['pts'] - entry['away']['pts'])

    M.append([1] * num_teams)
    y.append(0)

    return (np.array(M), np.array(y), team_index)


def rate_teams(data, team_index):
    columns = [None] * len(team_index)

    # place the team names into array at index matching their unique number
    for i in team_index.keys():
        columns[team_index[i]] = i
    ranks = zip(columns, data)
    ranks = list(reversed(sorted(ranks, key = lambda i: i[-1])))
    for i in range(len(ranks)):
        print('{:3} {:40} {:.2f}'.format(i+1, ranks[i][0], ranks[i][1]))


data = []
num_teams = 0
if len(sys.argv) != 2:
    data = parse_stats(input('Please enter the name of the data file:\t'))
else:
    data = parse_stats(sys.argv[1])

M,y,team_index = generate_matrices(data)

r = np.linalg.lstsq(M, y)[0]
rate_teams(r, team_index)
