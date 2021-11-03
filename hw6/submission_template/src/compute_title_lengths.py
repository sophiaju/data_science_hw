import json
import argparse

def main():

    # get input path
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help = "add the name of the input file", action="store")
    args = parser.parse_args()
    input_path = args.input

    with open(input_path, 'r') as infile:
        
        total_words = 0
        total_posts = 0

        # line by line, 
        for line in infile:
            post = json.loads(line)
            title = post['data']['title']
            # print(title, len(title.split()))
            
            # add the number of words in that title to total words
            total_words += len(title)
            # count the number of posts
            total_posts += 1
            
        # print(total_words, total_posts)

        # calculate avg title length and print!
        avg_title_len = total_words/total_posts
        print(avg_title_len)

        
if __name__ == '__main__':
    main()