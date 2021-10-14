import pandas as pd
from pathlib import Path
import os, sys
import json
import argparse, datetime
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def main(): 
    # default output file name
    output_file = "output.csv"

    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help = "add the name of the output file", action="store")
    parser.add_argument('data', help = "add name of dialog data file", action="store")
    args = parser.parse_args()
    if args.output:
        output_file = args.output
    data_file = args.data


    # gets path to the data csv
    data_path = os.path.join(parentdir, 'data', data_file)
    df = pd.read_csv(data_path, names=['id','opened','closed','zip'], header=None)

    # make zip into ints
    df['zip'] = df['zip'].astype(int)

    # find incident duration for each row and convert to hours
    df['duration'] = (pd.to_datetime(df['closed'])-pd.to_datetime(df['opened'])).astype('timedelta64[h]')

    # drop any negative durations
    df.drop(df[df['duration']<0].index, inplace=True)

    # find what month SR was closed
    df['month'] = pd.to_datetime(df['closed']).dt.month

    # group by month to get all 2020 data
    month = df.groupby(['month'])['duration'].mean()
    print(month)
    month.to_csv("all_2020.csv", index=True)
    print('file processed by month saved')

    # group by month and zipcode
    zip_month = df.groupby(['zip','month'])['duration'].mean().reset_index()
    print(zip_month)

    # save zip, month, avg, to csv
    zip_month.to_csv(output_file, index=False)

    # output path
    # out_path = os.path.join(parentdir, output_file)
    # # produce a JSON file
    # with open (out_path, 'w') as outfile:
    #     json.dump(zip_month, outfile, indent=4)
    # print('file processed by zip and month saved')




if __name__ == '__main__':
    main()