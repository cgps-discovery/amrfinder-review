import csv
import json 
import argparse
import os 

TAX_IDS = "1280    1313    1352    149539     194     287     354276  470     485     562     573     620     727     90370   90371".split()

def get_tax_id(accession, samplesheet):
    with open(samplesheet, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        tax_id = [(row['taxid'], row['ori_species']) for row in reader if row['sample'] == accession] 
        if tax_id: 
            return tax_id[0][0], tax_id[0][1]
        else:
            return None, None

def get_real_results(accession, tax_id):
    with open(f'organisms/{tax_id}/amrfinder.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        real_results = [row for row in reader if row['accession_id'] == accession] 
        if real_results: 
            return real_results[0]
        else:
            return None

def check_mappings(input_genes, tax_id): 
    raw_genes = input_genes.split(';')
    final_mapping = None
    correct_rules = json.loads(open(f'curated_mechanisms.json').read())
    count_tax_id = len([rule[0] for rule in correct_rules if tax_id == rule[0]])
    if count_tax_id == 0:
        final_mapping = 'No rulesheet'
    else:
        for rule in correct_rules:
            if set(raw_genes) == set(rule[3]) and tax_id == rule[0]:
                final_mapping = rule[2]
    if not final_mapping:
        final_mapping = 'none'
    if final_mapping[0] == ';':
        final_mapping = final_mapping[1:]
    return final_mapping


def RENAME(record, tax_id):
    if tax_id == '485':
        record['FLUOROQUINOLONE'] = record['QUINOLONE']
    return record




def main(args):
    print('accession', 'species','taxid', 'drug', 'expected', 'actual', 'passed', 'raw', sep='\t')
    with open(args.file, 'r') as amr_finder_filtered:
        reader = csv.DictReader(amr_finder_filtered)
        for record in reader:
            accession = record['accession_id'].split('_')[0]
            tax_id, species = get_tax_id(accession, args.sample_sheet)
            TAX_IDS_z = ['354276']
            if tax_id in TAX_IDS_z:
                real_results = get_real_results(accession, tax_id)
                record = RENAME(record, tax_id)
                if real_results:
                    ori_accession = real_results.pop('accession_id')
                    for key, value in real_results.items():
                        if record.get(key): 
                            final_prediction = check_mappings(record[key], tax_id)
                            passed = final_prediction == value
                            print(accession, species, tax_id, key, value, final_prediction, passed, record[key], sep='\t')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', type=str, help='The path to the short file to process, use convert_amr_finder', default='test_results/all_short.txt')
    parser.add_argument('--sample_sheet', type=str, help='The path to the samplesheet, with taxids', default='all_sample_data.csv')
    args = parser.parse_args()
    main(args)

            