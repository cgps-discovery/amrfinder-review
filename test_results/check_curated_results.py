import csv
import argparse
import os 
import subprocess 
import sys 

TAX_IDS = ['485' ,'354276' '287', '470',  '1280'] 
TAX_IDS = ['354276' ] 


def get_real_results(accession, tax_id):
    with open(f'organisms/{tax_id}/amrfinder.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        real_results = [row for row in reader if row['accession_id'] == accession] 
        if real_results: 
            return real_results[0]
        else:
            return None

def main(args):
    
    # Pick test data set 
    import random
    test_data = [x for x in csv.DictReader(open(args.sample_sheet)) if x['taxid'] in TAX_IDS] 
    if args.subsample < len(test_data):
        test_data = random.sample(test_data, args.subsample)
    print(f'Loaded {len(test_data)}', file=sys.stderr)
    print('accession', 'species','taxid', 'drug_class', 'expected', 'actual', 'passed', sep='\t')
    for test in test_data:
        results_file = results_file = os.path.join(args.file, test['sample'] + '_amrfinder.txt')
        accession = test['sample']
        species = test['ori_species']
        tax_id = test['taxid']
        if os.path.exists(results_file):            
            original_results = get_real_results(accession, tax_id)
            #  docker run --interactive test --curated --tax-id 287 --existing  < test_amr/amrfinder_test/DRR021823_amrfinder.txt
            # happykhan/amrfinder:amrfinder-2.2.0-runtime
            amrfinder_output = subprocess.run(['docker', 'run', '--platform=linux/x86_64', '--interactive', 'happykhan/amrfinder:amrfinder-2.3.0-runtime', '--curated', '--tax-id', tax_id, '--existing' ], input=bytes(open(results_file).read(), 'utf-8'), capture_output=True)
            if amrfinder_output.stderr:
                print(f'Something has gone wrong ({accession}, {tax_id}): ', file=sys.stderr)
                print(amrfinder_output.stderr, file=sys.stderr)
            elif original_results:
                import json 
                all_prediction = json.loads(amrfinder_output.stdout.decode('utf-8'))
                accession = original_results.pop('accession_id')
                for drug_class, genes in original_results.items():
                    this_prediction = ';'.join(sorted(all_prediction.get(drug_class, ['none'])))
                    sorted_genes = ';'.join(sorted(genes.split(';')))
                    passed = this_prediction == sorted_genes
                    if args.failed_only:
                        if not passed:
                            print(accession, species, tax_id, drug_class, sorted_genes, this_prediction, passed, sep='\t')
                    else:
                        print(accession, species, tax_id, drug_class, sorted_genes, this_prediction, passed, sep='\t')
            else:
                print(f'No original results for {accession}', file=sys.stderr)
        else:
            print(f'No results file {accession}', file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', type=str, help='The path to a folder of amrfinder (runtime results)', default='test_amr/amrfinder_test')
    parser.add_argument('--sample_sheet', type=str, help='The path to the samplesheet, with taxids', default='all_sample_data.csv')
    parser.add_argument('--curated', type=str, help='The path curated mechanisms filter as a json', default='curated_mechanisms.json')
    parser.add_argument('--failed_only', type=str, help='Show only failed results', default=False)
    parser.add_argument('--subsample', type=int, help='Run a subsample', default=1000000)
    args = parser.parse_args()
    main(args)

            
