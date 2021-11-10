import argparse
import json
import sys, os
import csv
import random

def parse_and_write(file, datawriter):

    for line in file:
        post = json.loads(line)
        name = post['data']['name']
        title = post['data']['title']

        datawriter.writerow([name, title])

def main():

    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help = "add the name of the output file", action="store")
    parser.add_argument('json', help="the json file to read in")
    parser.add_argument('num_posts', help='the number of posts to output', type=int)
    args = parser.parse_args()
    output_path = args.output
    json_file = args.json
    num_posts = args.num_posts


    # make output file directories
    if not os.path.exists(os.path.dirname(output_path)):
        if os.path.dirname(output_path) != '':
            os.makedirs(os.path.dirname(output_path))

    with open(output_path, 'w') as output:
        titlewriter = csv.writer(output, delimiter='\t',lineterminator='\n')
        # write first line
        titlewriter.writerow(['Name', 'title', 'coding'])
        datawriter = csv.writer(output, delimiter='\t', lineterminator='\t\n')

        with open(json_file) as infile:

            # get the number of posts in the file
            all_jsons = infile.readlines()
            infile_len = len(all_jsons)

            # if the number of wanted posts is greater that the number of json posts
            if num_posts > infile_len:

                # line by line, write the post name and title to csv
                parse_and_write(all_jsons, datawriter)
            
            # randomly select number of output posts
            else:
                sample = random.sample(all_jsons, num_posts)

                # line by line, write the post name and title to csv
                parse_and_write(sample, datawriter)

if __name__ == '__main__':
    main()