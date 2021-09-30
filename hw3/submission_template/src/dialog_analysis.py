import pandas as pd
from pathlib import Path
import os, sys
import json
import argparse
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

# print(parentdir)
# print(sys.path)
# print(dialog_file_path)
output_file = "output.json"

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help = "add the name of the output file", action="store")
parser.add_argument('data', help = "add name of dialog data file", action="store")
args = parser.parse_args()
if args.output:
    output_file = args.output
data_file = args.data

# print(args.output)
# print(args.data)


# gets path to the data csv
data_path = os.path.join(parentdir, 'data', data_file)
df = pd.read_csv(data_path)
# print(list(df.columns))

# print(df['pony'].value_counts()[:15])

# dictionary of the counts for our 6 main ponies
count_dict = {
    'twilight sparkle' : int(df['pony'].value_counts()['Twilight Sparkle']),
    'applejack' : int(df['pony'].value_counts()['Applejack']),
    'rarity' : int(df['pony'].value_counts()['Rarity']),
    'pinkie pie' : int(df['pony'].value_counts()['Pinkie Pie']),
    'rainbow dash' : int(df['pony'].value_counts()['Rainbow Dash']),
    'fluttershy' : int(df['pony'].value_counts()['Fluttershy']),
}

# print(count_dict)

total = len(df)

# dictionary of verbosity for each pony, count / total number of lines
verb_dict = {
    'twilight sparkle' : float(round(count_dict['twilight sparkle'] / total, 2)),
    'applejack' : float(round(count_dict['applejack'] / total, 2)),
    'rarity' : float(round(count_dict['rarity'] / total, 2)),
    'pinkie pie' : float(round(count_dict['pinkie pie'] / total, 2)),
    'rainbow dash' : float(round(count_dict['rainbow dash'] / total, 2)),
    'fluttershy' : float(round(count_dict['fluttershy'] / total, 2)),
}

# print(verb_dict)

# put into a final dictionary
result = {
    "count" : count_dict,
    "verbosity" : verb_dict
}

# print(result)
# output path
out_path = os.path.join(parentdir, output_file)

# produce a JSON file
with open (out_path, 'w') as outfile:
    json.dump(result, outfile)