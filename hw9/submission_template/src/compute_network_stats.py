from networkx.algorithms.centrality import betweenness
from networkx.algorithms.shortest_paths import weighted
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

    net_stats = {}

    with open(input_path, 'r') as infile:
        interactions = json.load(infile)

    # create network
    G = nx.Graph()

    for pony1 in interactions.keys():
        for pony2 in interactions[pony1].keys():

            # if the edge isn't already, add it
            if not G.has_edge(pony1, pony2):
                G.add_edge(pony1, pony2, weight=interactions[pony1][pony2])

    # print(f'Num nodes:{len(G)}')
    # print(f'Num edges:{G.size()}')

    # get top three most connected characters by number of edges
    pony_deg = {}
    for pony in G.nodes():
        pony_deg[pony] = G.degree(pony, weight=None)

    deg_list = list(pony_deg.items())
    deg_list.sort(key=lambda x: -x[-1])

    net_stats["most_connected_by_num"] = [deg_list[0][0], deg_list[1][0], deg_list[2][0]]

    # get top three most connected characters by the sum of the weight of edges
    pony_weight = {}
    for pony in G.nodes():
        pony_weight[pony] = G.degree(pony, weight='weight')

    weight_list = list(pony_weight.items())
    weight_list.sort(key=lambda x: -x[-1])

    net_stats["most_connected_by_weight"] = [weight_list[0][0], weight_list[1][0], weight_list[2][0]]
    
    # get top three most central characters by betweenness
    betw_centr_dict = betweenness.betweenness_centrality(G)
    betw_list = list(betw_centr_dict.items())
    betw_list.sort(key=lambda x: -x[-1])

    net_stats["most_central_by_betweenness"] = [betw_list[0][0], betw_list[1][0], betw_list[2][0]]

    # print(net_stats)


    # # produce a JSON file
    with open(output_path, 'w') as outfile:
        json.dump(net_stats, outfile, indent=4)


if __name__ == '__main__':
    main()