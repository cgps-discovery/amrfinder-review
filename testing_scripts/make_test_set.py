import os 
import random 
import csv

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


database_info = {
    '470':'Acinetobacter_baumannii',
    '562':'Escherichia',
    '1496': 'Clostridioides_difficile',
    '354276': None,
    '573':'Klebsiella', # Klebsiella is split between pneumoniae and oxytoca in one version, and kept as a single Klebsiella database in another
    '287':'Pseudomonas_aeruginosa',
    '194':'Campylobacter',
    '195':'Campylobacter', # campylobacter_coli
    '197':'Campylobacter', # campylobacter_jejuni
    '547': None, # enterobacter
    '354276': None, # Enterobacter cloacae complex
    '727': None, # hinfluenzae
    '210': None, # hpylori
    '1773': None, # mtuberculosis
    '1351':'Enterococcus_faecalis',
    '1352':'Enterococcus_faecium',
    '485':'Neisseria',
    '1280':'Staphylococcus_aureus',
    '283734': 'Staphylococcus_pseudintermedius',
    '1311':'Streptococcus_agalactiae',
    '149539':'Salmonella', # salmonella_enteritidis
    '90370':'Salmonella', # styphi
    '90371':'Salmonella', # salmonella_typhimurium
    '590':'Salmonella',
    '1314':'Streptococcus_pyogenes',
    '727': None, #hinfl
    '1313':'Streptococcus_pneumoniae',
    '620':'Escherichia', #shigella
    '623':'Escherichia', #shigella_flexneri
    '624':'Escherichia', #shigella_sonnei
    '666': 'Vibrio_cholerae',
    None:None
}


final_sample_list = [] 
# get list of possible gene profiles for each class 
classes = [] 
final_sample_record = []
PERCENT_BACKFILL = 0.02
TESTING_ORI_DIR = 'testing_ori'
TESTING_RESULTS_DIR = 'testing_results'

for organism_path, tax_id in [(os.path.join(TESTING_ORI_DIR, x,), x.split('-')[1].split('.')[0] ) for x in os.listdir(TESTING_ORI_DIR)] :
    records = csv.DictReader(open(organism_path)) 
    all_profiles = {}  
    total_records = 0 
    remaining_accessions = [] 
    csv_data = {} 
    for record in records:
        total_records += 1 
        
        accession = record.pop('accession_id')
        csv_data[accession] = record
        for k, v in record.items():
            index = f'{k}-{v}'
            if all_profiles.get(index):
                remaining_accessions.append(accession)
            else:
                # pick one per profile
                all_profiles[index] = accession
    
    remaining_accessions = list(set(remaining_accessions))
    # round up to 5 % of original data 
    subsample_number = round(total_records * PERCENT_BACKFILL) - len(all_profiles)
    additional_genomes_add = [] 
    if subsample_number > 0:
        additional_genomes_add = random.sample(remaining_accessions, subsample_number)
    final_genome_list = list(set(list(all_profiles.values()) + additional_genomes_add))
    for genome in final_genome_list:
        species = taxid_dict.get(tax_id)
        if type(species) == list:
            species = species[0]
        record = {'sample': genome, 'species': species, 'database': database_info.get(tax_id), 'taxid': tax_id,  **csv_data[genome]  }
        classes = list(set(classes + list(csv_data[genome].keys())))
        final_sample_record.append(record)

sample_sheet = csv.DictWriter(open(f'{TESTING_RESULTS_DIR}/full_samplesheet.csv', 'w'), fieldnames=['sample', 'species', 'database', 'taxid' ] + classes)    
sample_sheet.writeheader()
sample_sheet.writerows(final_sample_record)
