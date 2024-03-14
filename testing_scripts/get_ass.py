taxid_dict = {
    '1280': 'staphylococcus_aureus',
    '1313': 'streptococcus_pneumoniae', 
    '1352': 'enterococcus_faecium',
    '149539': 'salmonella_enteritidis',
    '287': 'pseudomonas_aeruginosa', 
    '354276': 'enterobacter', 
    '470': 'acinetobacter_baumannii', 
    '485': 'neisseria_gonorrhoeae', 
    '194': ['campylobacter', 'campylobacter_coli', 'campylobacter_jejuni'],
    '562': [ 'escherichia_coli', 'ecoli_shigella' ], 
    '573': ['klebsiella', 'klebsiella_pneumoniae' ],
    '620': ['shigella', 'shigella_flexneri', 'shigella_sonnei'], 
    '727': 'hinfluenzae', 
    '90370': 'styphi', 
    '90371': 'salmonella_typhimurium',
}

TESTING_RESULTS_DIR = 'testing_results'
samplesheet = f'{TESTING_RESULTS_DIR}/full_samplesheet.csv'
base_dir = "/well/aanensen/projects/amr-landscape/assemblies"
# /well/aanensen/projects/amr-landscape/assemblies/pseudomonas_aeruginosa/production/fasta_passed_qc/SRR9842281.fasta

import csv 
import os 
import sys 

new_records = [ ] 
print(f'opening testing dir {samplesheet}' )
fieldnames = ['sample', 'species', 'database', 'taxid', 'CARBAPENEM','QUINOLONE','CEPHALOSPORIN','FLUOROQUINOLONE','BETA-LACTAM','METHICILLIN','VANCOMYCIN', 'fasta']
for record in csv.DictReader(open(samplesheet))[0:10]: 
    taxid = record['taxid']
    accession = record['sample']
    folder = taxid_dict.get(taxid) 
    if type(folder) == list: 
        for fold in folder: 
            fasta_file = os.path.join(base_dir, fold,'production', 'fasta_passed_qc', f'{accession}.fasta' )
            if os.path.exists(fasta_file):
                print(f'found file {fasta_file}' )
                break; 
    else:
        fasta_file = os.path.join(base_dir, taxid_dict.get(taxid),'production', 'fasta_passed_qc', f'{accession}.fasta' )
        print(f'found file {fasta_file}' )
    if os.path.exists(fasta_file):
        record['fasta'] = fasta_file 
        new_records.append(record)
    else:
        print(f'file for accession {accession} not found at {fasta_file}', file=sys.stderr)

sample_sheet = csv.DictWriter(open(f'{TESTING_RESULTS_DIR}/full_samplesheet_fasta.csv', 'w'), fieldnames=fieldnames)    
sample_sheet.writeheader()
sample_sheet.writerows(new_records)

