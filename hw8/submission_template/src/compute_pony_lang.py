import pandas as pd
from pathlib import Path
import os, sys
import json, csv, math
import argparse
parentdir = Path(__file__).parents[1]

def get_tfidf(word_counts, num_words):
    pony_names = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash','fluttershy']

    all_word_counts = {}
    # print(word_counts['applejack'])
    # all_words = []

    # get all words and counts across all ponys
    for pony in pony_names:
        for word in word_counts[pony].keys():
            # if word not in all word count dict
            if word not in all_word_counts.keys():
                all_word_counts[word] = word_counts[pony][word]
            else:
                all_word_counts[word] += word_counts[pony][word]

    # print(json.dumps(all_word_counts, indent=4))
    # print(all_word_counts['twilight'])

    tfidf_dict = {}
    # print(len(word_counts))

    for pony in pony_names:
        tfidf_dict[pony] = {}
        for word in word_counts[pony].keys():
            
            # calculate tfidf

            # find number of ponies that use word
            num_pony = 0
            for all_pony in pony_names:
                if word in word_counts[all_pony].keys():
                    num_pony += 1
            # print(num_pony, word)

            # calculate tfidf
            tf = word_counts[pony][word]
            idf = math.log(len(word_counts)/num_pony, 10)
            tfidf = tf * idf

            tfidf_dict[pony][word] = tfidf

    # print(json.dumps(tfidf_dict['fluttershy'], indent=4))
    # with open('tfidf.json', 'w') as file:
    #     json.dump(tfidf_dict, file, indent=4)

    results = {}

    # sort by tfidf and get top num_words
    for pony in tfidf_dict:
        sorted_dict = sorted(tfidf_dict[pony], key=tfidf_dict[pony].get, reverse=True)
        trimmed = sorted_dict[0:num_words]
        results[pony] = trimmed

    return results



def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--counts", help = "add the name of the counts file", action="store")
    parser.add_argument('-n', '--num', help = "add number of top tfidf words", action="store")
    args = parser.parse_args()
    counts_path = args.counts
    num_words = int(args.num)

    # read in counts JSON file
    with open (counts_path, 'r') as infile:
        word_counts = json.load(infile)

    results = get_tfidf(word_counts, num_words)

    print(json.dumps(results, indent=4))




if __name__ == '__main__':
    main()