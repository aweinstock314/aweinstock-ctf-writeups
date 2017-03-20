#!/usr/bin/env python
import json
import requests
import sys

x = requests.get('http://mitctf.com/scoreboard_data.php')

with open('mitctf_scores.json', 'w') as f:
    f.write(x.text)

y = json.loads(x.text)

rows = y['rows'] if '--all' in sys.argv else [y['rows'][-1]]

for j, row in enumerate(rows):
    for i, col in sorted(enumerate(y['cols']), key=lambda (i,_): row['c'][i]['v'], reverse=True):
        if i == 0:
            print("At time %s:" % row['c'][i]['v'])
        else:
            print("\tTeam %r had score %d" % (col['label'], row['c'][i]['v']))
