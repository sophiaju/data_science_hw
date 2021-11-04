import json, requests
import os, sys
import argparse
import bs4
from bs4 import BeautifulSoup

BASE_URL = "https://www.whosdatedwho.com/dating/"

# given a list of href links, extract the names and add to dict
def add_just_name(dict, list_names, person):

    for name in list_names:
        just_name = name['href'].split("/")[2]

        # if it is not the own person's name, add to dictionary
        if just_name != person:
            dict[person].append(just_name)


def main():

    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True, help = "add the name of the config file", action="store")
    parser.add_argument("-o", "--output", required=True, help = "add the name of the output file", action="store")
    args = parser.parse_args()
    output_path = args.output
    config_path = args.config

    # read config file
    with open(config_path, 'r') as config:
        config_json = json.load(config)

    # get cache directory
    cache_dir = config_json['cache_dir']
    
    # if cache directory does not exist, make one
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # dictionary for output file
    output_dict = {}

    # for every target person in config file
    for person in config_json['target_people']:
        print(person)

        # initialize that person in dict
        output_dict[person] = []

        # name for created cache
        person_cache = os.path.join(cache_dir, person + '.html')

        # if cache is not there, make one
        if not os.path.exists(person_cache):

            url = f'{BASE_URL}{person}'
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

            print('fetching', url)

            r = requests.get(url, headers=headers)
            page_content = r.text

            with open (person_cache, 'w', encoding='utf-8') as file:
                file.write(page_content)

        # if cache is there, load from file
        else:
            print('loading from cache')
            with open(person_cache, 'rb') as file:
                page_content = file.read()

        # make soup!
        soup = BeautifulSoup(page_content, 'html.parser')

        # find current relationship status header
        status_h4 = soup.find('h4', class_='ff-auto-status')

        # get names under current relationship status
        curr_rel_names = status_h4.next_sibling.find_all('a', href=True, style=False)

        # for each name in current relationship section, get names and add to dict
        add_just_name(output_dict, curr_rel_names, person)

        # find past relationships header
        relationships = soup.find('h4', class_='ff-auto-relationships')

        # get paragraphs after header
        rel_p = relationships.find_next_siblings('p', class_=False)

        # for each paragraph, find href links and add names to dict
        for p in rel_p:
            past_rels = p.find_all('a', href=True, style=False)
            add_just_name(output_dict, past_rels, person)

    # dump to json file
    with open(output_path, 'w') as outfile:
        json.dump(output_dict, outfile, indent=4)



if __name__ == '__main__':
    main()