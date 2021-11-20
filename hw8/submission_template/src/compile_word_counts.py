import pandas as pd
from pathlib import Path
import os, sys
import json, csv
import argparse
parentdir = Path(__file__).parents[1]
# sys.path.append(parentdir)

def get_word_counts(data_path, freq_thresh):

    # load in dialog
    df = pd.read_csv(data_path)

    # make stopwords path
    stop_path = os.path.join(parentdir,'data','stopwords.txt')
    stop_words = []

    # load in stopwords
    with open(stop_path, 'r') as stop_file:
        stop_reader = csv.reader(stop_file)
        for line in stop_reader:
            if '#' not in line[0]:
                stop_words.append(line[0])

    word_counts = {}

    pony_names = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash','fluttershy']

    all_words = []

    punct = ['(', ')', '[',']',',','-','.','?','!',':',';','#','&']

    # for each pony
    for pony in pony_names:

        # set up word count dictionary
        word_counts[pony] = {}

        dialog = df.loc[df['pony'].str.contains(f'^{pony}$', case=False, regex=True)]['dialog']
        
        for line in dialog:
            
            # split line by spaces
            words = line.split(' ')

            # clean words
            for word in words:
                cleaned = "".join([x.lower() if x not in punct else " " for x in word])
                split = cleaned.split(' ')
                # for each stripped word
                for stripped in split:
                    # get rid of stopwords and words with non alphabetic characters
                    if stripped not in stop_words and stripped.isalpha():
                        all_words.append(stripped)
                        # add to word count dictionary
                        if stripped in word_counts[pony].keys():
                            word_counts[pony][stripped] += 1
                        else:
                            word_counts[pony][stripped] = 1
                            # get rid of words that have less than 5 occurances across all speech acts
    for w in all_words:
        total_count = 0
        # count total occurences of the word
        for pony in pony_names:
            if w in word_counts[pony].keys():
                total_count += word_counts[pony][w]
        # if not requent enough, remove from all pny word counts
        if total_count < freq_thresh:
            for pony in pony_names:
                word_counts[pony].pop(w, None)

    return(word_counts)

def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help = "add the name of the output file", action="store")
    parser.add_argument('-d', '--data', help = "add name of dialog data file", action="store")
    args = parser.parse_args()
    output_path = args.output
    data_path = args.data

    # make output file directories
    if not os.path.exists(os.path.dirname(output_path)):
        if os.path.dirname(output_path) != '':
            os.makedirs(os.path.dirname(output_path))

    # load in dialog
    # df = pd.read_csv(data_path)
    # print(df)

    word_counts = get_word_counts(data_path, 5)

    # produce a JSON file
    with open (output_path, 'w') as outfile:
        json.dump(word_counts, outfile, indent=4)


if __name__ == '__main__':
    main()