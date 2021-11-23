import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
import os, sys
import json, csv
import argparse
parentdir = Path(__file__).parents[1]
# sys.path.append(parentdir)


def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help = "add name of dialog data file", action="store")
    parser.add_argument("-o", "--output", help = "add the name of the output file", action="store")    
    args = parser.parse_args()
    output_path = args.output
    input_path = args.input

    # make output file directories
    if not os.path.exists(os.path.dirname(output_path)):
        if os.path.dirname(output_path) != '':
            os.makedirs(os.path.dirname(output_path))

    # load in dialog
    df = pd.read_csv(input_path)
    # print(df[['pony','dialog']])

    # make all names lowercase
    df['pony'] = df['pony'].str.lower()

    # list of stopwords
    stopwords = ["others", "ponies", "and", "all"]

    # get counts of all pony dialog and sorts
    all_counts = df['pony'].value_counts().to_dict()
    
    # leave only valid characters in all_counts dict
    for pony_name in list(all_counts):
        pony_name_words = pony_name.split(" ")

        # remove the names with "others", "ponies", "and", "all"
        for word in pony_name_words:
            if word in stopwords and pony_name in all_counts.keys():
                all_counts.pop(pony_name)

    # print(np.array((list(all_counts.items())[0:101]))[:,0])
    # top 101 characters with valid names
    top_101 = np.array((list(all_counts.items())[0:101]))[:,0]

    # group by episode title
    df_grouped = df.groupby('title')
    # print(df_grouped.get_group('Friendship is Magic, part 1'))
    # print(df_grouped.ngroups)

    interactions = {}

    for group in df_grouped:

        # group = df_grouped.get_group('Friendship is Magic, part 1')
        # print(group[['pony']])
        # print(group[1])

        line_speakers = np.array(group[1]['pony'])
        # print(np.array(group['pony']))

        for i in range(0,len(line_speakers)-1):
            # print(line_speakers[i],",", line_speakers[i+1])
            pony1 = line_speakers[i]
            pony2 = line_speakers[i+1]

            # if both pony names valid and not identical, add to interaction dict
            if pony1 in top_101 and pony2 in top_101 and pony1 != pony2:

                if pony1 not in interactions.keys():
                    interactions[pony1] = {}
                if pony2 not in interactions.keys():
                    interactions[pony2] = {}

                if pony2 not in interactions[pony1].keys():
                    interactions[pony1][pony2] = 1
                else:
                    interactions[pony1][pony2] += 1

                if pony1 not in interactions[pony2].keys():
                    interactions[pony2][pony1] = 1
                else:
                    interactions[pony2][pony1] += 1

    # print(json.dumps(interactions, indent=4))
    # print(len(list(interactions.keys())))

    # produce a JSON file
    with open(output_path, 'w') as outfile:
        json.dump(interactions, outfile, indent=4)


if __name__ == '__main__':
    main()