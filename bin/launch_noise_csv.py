#!/usr/bin/env python3

import argparse
import json
from src.data.csv import CsvProcessing
import src.data.experiments as exp


def get_args():

    "get the arguments when using from the commandline"
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-c", "--csv", type=str, required=True, metavar="FILE", help='The file path for the csv containing all data')
    parser.add_argument("-j", "--json", type=str, required=True, metavar="FILE", help='The json config file that hold all parameter info')
    parser.add_argument("-o", "--output", type=str, required=True, metavar="FILE", help='The output file path to write the noised csv')

    args = parser.parse_args()
    return args




def main(data_csv, config_json, out_path):
    """
    This launcher will be the connection between the csv and one json configuration.
    It should also handle some sanity checks.

    TODO what happens when the user write his own experiment class? how should he do it ? how does it integrates here?
    """
    
    # open and read Json
    config = {}
    with open(config_json, 'r') as in_json:
        config = json.load(in_json)

    # initialize the experiment class
    exp_obj = getattr(exp, config["experiment"])() 

    # initialize the csv processing class, it open and reads the csv in automatic 
    csv_obj = CsvProcessing(exp_obj, data_csv)
    
    # noise the data according to what defined in the experiment class and the specifics of the user in the Json
    # in case of no noiser specification so when the config has "noise" : None  just save a copy of the original csv file, hat will later be removed by the pipeline when the split has been performed
    if config["noise"]: 
        csv_obj.add_noise(config["noise"])

    # save the modified csv
    csv_obj.save(out_path)





if __name__ == "__main__":
    args = get_args()
    main(args.csv, args.json, args.output)
