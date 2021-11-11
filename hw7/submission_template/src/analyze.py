import argparse
import json
import os
import csv

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=False, help = "add the name of the output file", action="store")
    parser.add_argument("-i", "--input", required=True, help = "add the name of the annotated file", action="store")
    args = parser.parse_args()
    if args.output:
        output_path = args.output
        # make output file directories if they don't exist
        if not os.path.exists(os.path.dirname(output_path)):
            if os.path.dirname(output_path) != '':
                os.makedirs(os.path.dirname(output_path))
    input_path = args.input

    freq_dict = {"course-related":0, "food-related":0, "residence-related":0, "other":0}

    with open(input_path, 'r') as infile:
        datareader = csv.DictReader(infile, delimiter='\t')

        for post in datareader:
            coding = post['coding']
            if coding == 'c':
                freq_dict["course-related"] += 1
            if coding == 'f':
                freq_dict["food-related"] += 1
            if coding == 'r':
                freq_dict["residence-related"] += 1
            if coding == 'o':
                freq_dict["other"] += 1
        

    # if given an output file
    if args.output:

        with open(output_path, 'w') as output:

            json.dump(freq_dict, output, indent=4)

    else:
        print(json.dumps(freq_dict, indent=4))


if __name__ == '__main__':
    main()