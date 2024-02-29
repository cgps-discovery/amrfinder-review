import os
import subprocess
import csv

def get_tax_id(accession):
    with open('large_sample_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        tax_id = [(row['taxid'], row['ori_species']) for row in reader if row['sample'] == accession] 
        if tax_id: 
            return tax_id[0][0], tax_id[0][1]
        else:
            return None, None

TAX_IDS = "1280    1313    1352    149539     194     287     354276  470     485     562     573     620     727     90370   90371".split()

def get_real_results(accession, tax_id):
    with open(f'organisms/{tax_id}/amrfinder.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        real_results = [row for row in reader if row['accession_id'] == accession] 
        if real_results: 
            return real_results[0]
        else:
            return None

print('accession', 'species','taxid', 'drug', 'expected', 'actual', 'passed', sep='\t')
with open('short', 'r') as amr_finder_filtered:
    reader = csv.DictReader(amr_finder_filtered)
    for record in reader:
        accession = record['accession_id'].split('_')[0]
        tax_id, species = get_tax_id(accession)
        if tax_id in TAX_IDS:
            real_results = get_real_results(accession, tax_id)
            if real_results:
                ori_accession = real_results.pop('accession_id')
                for key, value in real_results.items():
                    passed = record[key] == value
                    print(accession, species, tax_id, key, value, record[key], passed, sep='\t')

            
