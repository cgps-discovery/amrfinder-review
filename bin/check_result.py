#!/usr/bin/env python3
import json
import argparse
import csv 

def check_result(index, sample, samplejson):
    # Load the expected results
    expected_results = {x['sample']: x for x in csv.DictReader(open(index, 'r'))}
    expected_result = expected_results.get(sample, None)
    # Load the sample results
    with open(samplejson, 'r') as f:
        sample_results = json.load(f)
        if not sample_results:
            sample_results = {}

    for classes, value in expected_result.items():
        if classes in ['CARBAPENEM', 'QUINOLONE', 'CEPHALOSPORIN', 'FLUOROQUINOLONE', 'BETA-LACTAM', 'METHICILLIN', 'VANCOMYCIN'] and expected_result.get(classes):    
            value = ';'.join( sorted( value.split(';') )       )
            actual_result = ';'.join(sorted(sample_results.get(classes, ['none'])))
            passing = value == actual_result
            species = expected_result['species']
            database = expected_result['database']
            taxid = expected_result['taxid']
            print(f"{sample}\t{species}\t{database}\t{taxid}\t{classes}\t{value}\t{actual_result}\t{passing}")

def main():
    parser = argparse.ArgumentParser(description='Check results.')
    parser.add_argument('index', type=str, help='Path to the index.json file')
    parser.add_argument('sample', type=str, help='Path to the sample.txt file')
    parser.add_argument('samplejson', type=str, help='Path to the sample.json file')
    args = parser.parse_args()

    check_result(args.index, args.sample, args.samplejson)

if __name__ == "__main__":
    main()