#!/usr/bin/env python

__author__ = 'Benjamin Adams'
__version__ = '0.1'
__email__ = 'adamsbt@appstate.edu'
__credit__ = 'Benjamin Adams, Jenna Schachner, Gabriel Mercer'

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
	return data


def generate_matrices(data):
	new_M_row = [0 for i in range(4)]
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

		M.append(list(new_M_row))
		M[-1][team_index[entry['home']['team']]] = 1
		M[-1][team_index[entry['away']['team']]] = -1

		y.append(entry['home']['pts'] - entry['away']['pts'])

	return (np.array(M), np.array(y))

def pprint(lst):
	for row in lst:
		for item in row:
			print(item, end=' ')
		print()


data = []
if len(sys.argv) != 2:
	data = parse_stats(input('Please enter the name of the data file:\t'))
else:
	data = parse_stats(sys.argv[1])
M,y = generate_matrices(data)

print(np.dot(np.transpose(M), M))
print(np.dot(np.transpose(M), y))
r = np.linalg.lstsq(M, y)[0]
print(r)
pprint(M)
