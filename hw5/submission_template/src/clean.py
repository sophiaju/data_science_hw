from json.decoder import JSONDecodeError
from pathlib import Path
import os, sys, datetime, json, argparse
from datetime import timezone, datetime
import pytz
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def clean(line):

    try:
        jf = json.loads(line)
               
    # if line is not JSON decodable, skip line
    except JSONDecodeError:
        # print("no load")
        return(None)
    
    # make sure post has title or title_text field
    if ("title" in jf) or ("title_text" in jf):

        # if has title_text, rename to title
        if ("title_text" in jf):
            jf["title"] = jf.pop("title_text")

    # if no title field, remove
    else:
        # print("no title")
        return(None)

    # check if post has author
    if ("author" in jf):

        # if author field is present but empty, remove
        if (jf["author"] is None) or (jf["author"] == "N/A") or (jf["author"] == ""):
            # print(jf["title"], "author")
            return(None)

    # if createdAt field exists
    if ("createdAt" in jf):
        # convert datetime to UTC
        try:
            new_time = datetime.strptime(jf["createdAt"], '%Y-%m-%dT%H:%M:%S%z')
            jf["createdAt"] = new_time.astimezone(pytz.utc).isoformat()
        # if datetime cannot be parsed, remove
        except ValueError:
            # print(jf["title"], "datetime")
            return(None)
        
    # cast total_count to int
    if ("total_count" in jf):
            
        try:
            jf["total_count"] = int(jf["total_count"])
        except ValueError:
            # print(jf["title"], "cast to int")
            return(None)
    
    # parse the tags into individual words
    if ("tags" in jf):
        new_tag = []
        for tag in jf["tags"]:
            new_tag.extend(tag.split(" "))
        jf["tags"] = new_tag

    # print(jf["title"], "passed")
    return(jf)
    
    

def main():

    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "add the name of the input file", action="store")
    parser.add_argument("-o", "--output", help = "add the name of the output file", action="store")
    args = parser.parse_args()
    output_path = args.output
    input_path = args.input

    list_of_dicts = []

    with open(input_path) as infile:
            
        # line by line, load the json file into dictionaries
        for line in infile:
           
            # clean each dictionary
            cleaned = clean(line)
            if cleaned is not None:
                list_of_dicts.append(cleaned)
            

    # return the cleaned data as json on separate lines
    with open(output_path, 'w') as outfile:
        for dict in list_of_dicts:
            json.dump(dict, outfile)
            outfile.write("\n")
    
    return


if __name__ == '__main__':
    main()