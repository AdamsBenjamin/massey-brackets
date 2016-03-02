# !/usr/bin/env python
# encoding: utf-8

import numpy as np
import json
import os
import sys

__author__ = 'Benjamin Adams'
__version__ = '0.1'
__email__ = 'adamsbt@appstate.edu'
__credit__ = 'Benjamin Adams, Jenna Schachner, Gabriel Mercer'

def parse_stats(filename):
	# checks that the given file exists and is a valid format.
	if not os.path.isfile(filename) or not filename.endswith('.json'):
		print('Invalid path or file type.')
		sys.exit(1)

	# parses and saves the file data to an array.
	data = []
	with open(filename, 'r') as fp:
		data = json.load(fp)

	# returns a tuple of the array of dictionaries parsed from the json file
	# as well as a count of the number of teams.
	return (data, len(set([entry['home']['team'] for entry in data])))


def generate_matrices(data, num_teams):
	team_counter = 0
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
		M.append([0 for i in range(num_teams)])
		M[-1][team_index[entry['home']['team']]] = 1
		M[-1][team_index[entry['away']['team']]] = -1

		# adds the newest game's point difference, in terms of the
		# home team, to the end of the y vector.
		y.append(entry['home']['pts'] - entry['away']['pts'])

		#home team advantage correction
		if entry['home']['pts'] > entry['away']['pts']:
			y[-1] -= 2

	M.append([1 for i in range(num_teams)])
	y.append(0)

	return (np.array(M), np.array(y), team_index)


def rate_teams(data, team_index):
	columns = [None for i in range(len(data))]

	#place the team names into array at index matching their unique number
	for i in team_index.keys():
		columns[team_index[i]] = i
	ranks = zip(columns, data)
	ranks = list(reversed(sorted(ranks, key = lambda i: i[-1])))
	for i in range(len(ranks)):
		print(str(i+1) + ' ' + str(ranks[i][0]) + ' {:.2f}'.format(ranks[i][1]))


data = []
num_teams = 0
if len(sys.argv) != 2:
	data, num_teams = parse_stats(input('Please enter the name of the data file:\t'))
else:
	data, num_teams = parse_stats(sys.argv[1])

M,y,team_index = generate_matrices(data, num_teams)

r = np.linalg.lstsq(M, y)[0]
#print(r)
rate_teams(r, team_index)
