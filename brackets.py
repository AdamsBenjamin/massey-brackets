#!/usr/bin/env python

__author__ = 'Benjamin Adams'
__version__ = '0.1'
__email__ = 'adamsbt@appstate.edu'
__credit__ = 'Benjamin Adams, Jenna Schachner, Gabriel Mercer'

import pprint as pp
import numpy as np
import json
import os
import sys

def parse_stats(filename):
	#checks that the given file exists and is a valid format
	if not os.path.exists(filename) or not filename.endswith('.json'):
		print('Invalid path or file type.')
		sys.exit(1)

	#parses and saves the file data to a variable
	data = []
	with open(filename, 'r') as fp:
		data = json.load(fp)

	return (data, len(set(entry['home']['team'] for entry in data)))


def generate_matrices(data, num_teams):
	team_counter = 0
	M = []
	y = []
	team_index = {}

	#single-pass through all dictionaries in data array
	for entry in data:
		if entry['home']['team'] not in team_index.keys():
			team_index[entry['home']['team']] = team_counter
			#print(entry['home']['team'] + ': ' + str(team_index[entry['home']['team']]))
			team_counter += 1

		if entry['away']['team'] not in team_index.keys():
			team_index[entry['away']['team']] = team_counter
			#print(entry['away']['team'] + ': ' + str(team_index[entry['away']['team']]))
			team_counter += 1

		M.append([0 for i in range(num_teams)])
		M[-1][team_index[entry['home']['team']]] = 1
		M[-1][team_index[entry['away']['team']]] = -1

		y.append(entry['home']['pts'] - entry['away']['pts'])

	M.append([1 for i in range(num_teams)])
	y.append(0)

	return (np.array(M), np.array(y), team_index)


def rate_teams()
	pass


data = []
num_teams = 0
if len(sys.argv) != 2:
	data, num_teams = parse_stats(input('Please enter the name of the data file:\t'))
else:
	data, num_teams = parse_stats(sys.argv[1])

M,y,team_index = generate_matrices(data, num_teams)

r = np.linalg.lstsq(M, y)[0]
print(r)

