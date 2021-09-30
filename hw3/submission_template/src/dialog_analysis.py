import pandas as pd
from pathlib import Path
import os, sys
import json
import argparse
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

# default output file name
output_file = "output.json"

# parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help = "add the name of the output file", action="store")
parser.add_argument('data', help = "add name of dialog data file", action="store")
args = parser.parse_args()
if args.output:
    output_file = args.output
data_file = args.data


# gets path to the data csv
data_path = os.path.join(parentdir, 'data', data_file)
df = pd.read_csv(data_path)


# dictionary of the counts for our 6 main ponies
count_dict = {
    'twilight sparkle' : int(len(df.loc[df['pony'].str.contains('^twilight sparkle$', case=False, regex=True)])),
    'applejack' : int(len(df.loc[df['pony'].str.contains('^applejack$', case=False, regex=True)])),
    'rarity' : int(len(df.loc[df['pony'].str.contains('^rarity$', case=False, regex=True)])),
    'pinkie pie' : int(len(df.loc[df['pony'].str.contains('^pinkie pie$', case=False, regex=True)])),
    'rainbow dash' : int(len(df.loc[df['pony'].str.contains('^rainbow dash$', case=False, regex=True)])),
    'fluttershy' : int(len(df.loc[df['pony'].str.contains('^fluttershy$', case=False, regex=True)])),
}

# total number of speech events
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

# put into a final dictionary
result = {
    "count" : count_dict,
    "verbosity" : verb_dict
}


# output path
out_path = os.path.join(parentdir, output_file)

# produce a JSON file
with open (out_path, 'w') as outfile:
    json.dump(result, outfile, indent=4)