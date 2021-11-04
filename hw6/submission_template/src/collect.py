import requests, json

# function to generate json of posts given a list of subreddits and the path of output
def gen_json(list_subs, output_name):

    with open(output_name, 'w') as output:

        for sub in list_subs:

            url = f"https://www.reddit.com/r/{sub}/new.json?limit=100"
            print(sub)

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

            # get post json
            r = requests.get(url, headers=headers)
            root_element = r.json()
            posts = root_element['data']['children']

            # write posts to output file
            for post in posts:
                json.dump(post, output)
                output.write("\n")


def main():
    # sample 1 subreddits
    pop_subs = ["funny", "AskReddit", "gaming", "aww", "pics", "Music", "science", "worldnews","videos", "todayilearned"]

    # sample 2 subreddits
    pop_posts = ["AskReddit", "memes", "politics", "nfl", "nba", "wallstreetbets", "teenagers", "PublicFreakout", "leagueoflegends", "unpopularopinion"]

    # generate files
    gen_json(pop_subs, "sample1.json")
    gen_json(pop_posts, "sample2.json")
    
        

if __name__ == '__main__':
    main()

