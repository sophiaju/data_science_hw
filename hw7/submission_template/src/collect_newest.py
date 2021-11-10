import requests
import argparse
import json
import sys, os

def main():

    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=False, help = "add the name of the output file", action="store")
    parser.add_argument("-s", "--subreddit", required=True, help = "add the name of the subreddit: '/r/subreddit'", action="store")
    args = parser.parse_args()
    if args.output:
        output_path = args.output

    subreddit = args.subreddit

    url = f"https://www.reddit.com{subreddit}/new.json?limit=100"

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    # get post json
    r = requests.get(url, headers=headers)
    root_element = r.json()
    posts = root_element['data']['children']

    # if given an output file
    if args.output:

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        with open(output_path, 'w') as output:

        # write posts to output file
            for post in posts:
                json.dump(post, output)
                output.write("\n")
    else:
        for post in posts:
                print(json.dumps(post))




if __name__ == '__main__':
    main()