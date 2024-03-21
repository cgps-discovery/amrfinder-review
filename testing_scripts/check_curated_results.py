import csv
import argparse
import os 
import subprocess 
import sys 

CLASSES = ['CARBAPENEM', 'QUINOLONE', 'CEPHALOSPORIN', 'FLUOROQUINOLONE', 'BETA-LACTAM', 'METHICILLIN', 'VANCOMYCIN']

def main(args):
    
    # Pick test data set 
    import random
    test_data = [x for x in csv.DictReader(open(args.sample_sheet)) if x['taxid'] in args.taxid] 
    # filter with test_results.txt
    filter_list = [] 
    if not args.all:
        with open(f'{args.dir.split("/")[0]}/test_results.txt') as f:
            for line in f.readlines():
                line = line.strip()
                if line.split('\t')[7] == 'False' and line.split('\t')[3] in args.taxid:
                    filter_list.append(line.split('\t')[0])
        test_data = [x for x in test_data if x['sample'] in filter_list]

    print(f'Loaded {len(test_data)}', file=sys.stderr)
    print('accession', 'species','taxid', 'drug_class', 'expected', 'actual', 'passed', sep='\t')
    for test in test_data:
        results_file = os.path.join(args.dir, test['sample'] + '_amrfinder.txt')
        accession = test['sample']
        species = test['species']
        tax_id = test['taxid']
        if os.path.exists(results_file):            
            #  docker run --interactive test --curated --tax-id 287 --existing  < test_amr/amrfinder_test/DRR021823_amrfinder.txt
            # happykhan/amrfinder:amrfinder-2.3.0-runtime
            if args.script_only:
                amrfinder_output = subprocess.run(['python', '3.12.8/docker/run.py', '--curated', '--tax-id', tax_id, '--existing', '--tempdir', 'temp/'], input=bytes(open(results_file).read(), 'utf-8'), capture_output=True)
            else:
                amrfinder_output = subprocess.run(['docker', 'run', '--platform=linux/x86_64', '--interactive', 'happykhan/amrfinder:amrfinder-2.3.0-runtime', '--curated', '--tax-id', tax_id, '--existing' ], input=bytes(open(results_file).read(), 'utf-8'), capture_output=True)
            if amrfinder_output.stderr:
                print(f'Something has gone wrong ({accession}, {tax_id}): ', file=sys.stderr)
                print(amrfinder_output.stderr, file=sys.stderr)
            else:
                import json 
                all_prediction = json.loads(amrfinder_output.stdout.decode('utf-8'))
                for drug_class in CLASSES:
                    if test.get(drug_class):
                        genes = test.get(drug_class)
                        if drug_class == 'FLUOROQUINOLONE':
                            drug_class = 'QUINOLONE'
                        this_prediction = ';'.join(sorted(all_prediction.get(drug_class, ['none'])))
                        sorted_genes = ';'.join(sorted(genes.split(';')))
                        passed = this_prediction == sorted_genes
                        if args.failed:
                            if not passed:
                                print(accession, species, tax_id, drug_class, sorted_genes, this_prediction, passed, sep='\t')
                        else:
                            print(accession, species, tax_id, drug_class, sorted_genes, this_prediction, passed, sep='\t')
        else:
            print(f'No results file {accession}', file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', type=str, help='The path to a folder of amrfinder (table results)', default='testing_results_v2/amrfinder_test')
    parser.add_argument('--sample_sheet', type=str, help='The path to the samplesheet, with taxids', default='testing_datasets/full_samplesheet_fasta.csv')
    parser.add_argument('--curated_file', type=str, help='The path curated mechanisms filter as a json', default='curated_mechanisms.json')
    parser.add_argument('--taxid', type=str, help='taxid to filter', nargs='+', default=['573'])
    parser.add_argument('--failed', help='Show failed only', action='store_true', default=False)
    parser.add_argument('--script_only', help='dont use the container', action='store_true', default=True)
    parser.add_argument('--subsample', type=int, help='Run a subsample', default=1000000)
    parser.add_argument('--all', help='Do all', action='store_true', default=True)

    args = parser.parse_args()
    main(args)

            
