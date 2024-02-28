import os
import subprocess
import csv
import json 
import argparse
import sys 

def get_real_results(accession, tax_id):
    with open(f'organisms/{tax_id}/amrfinder.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        real_results = [row for row in reader if row['accession_id'] == accession] 
        if real_results: 
            return real_results[0]
        else:
            return None

def get_tax_id(accession, filename='species3_sample_data.csv'):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        tax_id = [(row['taxid'], row['ori_species']) for row in reader if row['sample'] == accession] 
        if tax_id: 
            return tax_id[0][0], tax_id[0][1]
        else:
            return None, None

def run(args):
    """
    Run the AMR (Antimicrobial Resistance) analysis for each JSON file in the specified directory.

    Args:
        args (object): The command-line arguments passed to the script.

    Returns:
        None
    """
    OLD_VERSION = args.old_version
    results_dir = args.results_dir
    tax_ids = args.tax_ids
    sample_sheet = args.sample_sheet
    print('accession', 'species','taxid', 'drug', 'expected', 'actual', 'passed', sep='\t')
    # Loop through each JSON file in the "amrfinder" directory
    for file in os.listdir(results_dir):
        if file.endswith(".json"):
            accession = file.split('_')[0]
            tax_id, species = get_tax_id(accession, sample_sheet)
            if tax_id: 
                if str(tax_id) in tax_ids:
                    # Run the file through Docker
                    if OLD_VERSION:
                        cmd = ["docker", "run", "--platform=linux/x86_64", "--rm", "-i", f'public.ecr.aws/e2u6m3q5/dev-tools:amrfinder-curator-1', tax_id]
                    else:
                        cmd = ["docker", "run", "--platform=linux/x86_64", "--rm", "-i", f'public.ecr.aws/e2u6m3q5/dev-tools:amrfinder-curator-{tax_id}']
                    results = subprocess.run(cmd, stdin=open(os.path.join(results_dir, file)), capture_output=True, text=True)
                    if results.stderr:
                        print(results.stderr, file=sys.stderr)
                        print(accession, species, tax_id, 'program error',  'program error',  'program error', False, sep='\t')
                    else:
                        final_results = json.loads(results.stdout)
                        real_results = get_real_results(accession, tax_id)
                        if real_results:
                            ori_accession = real_results.pop('accession_id')
                            for key, value in real_results.items():
                                actual_value = final_results.get(key, ['none'])
                                if actual_value: 
                                    actual_value = ';'.join(actual_value)
                                passed = actual_value == value
                                print(accession, species, tax_id, key, value, actual_value, passed, sep='\t')

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--old_version', type=bool, default=False,
                        help='A boolean switch to use old version')
    parser.add_argument('--sample_sheet', type=str, default='species3_sample_data.csv',
                        help='Sample sheet from the amrfinder run')
    parser.add_argument('--results_dir', type=str, default='amrfinder_run_3',
                        help='Json from the amrfinder run')
    parser.add_argument('--tax_ids', type=str, nargs='+', default=['287'])
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
