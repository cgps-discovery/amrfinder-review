import csv 
import os 

genes = {}
taxid = '573'

file_paths = ['testing_ori/amrfinder-573.csv' ]
records = [] 
for file_path in file_paths:
    records += [x for x in csv.DictReader(open(file_path))] 

for record in records:
    accession = record.pop('accession_id')
    for classes, value in record.items():
        if value != 'none':
            if genes.get(classes):
                genes[classes] = list(set(genes[classes] + value.split(';')))
            else:
                genes[classes] = value.split(';')
for classes, gene_list in genes.items():
    for g in gene_list: 
        if classes == 'FLUOROQUINOLONE':
             print(f'["{taxid}", ["QUINOLONE","FLUOROQUINOLONE"], "{g}", ["{g}"] ],')
        else:
            print(f'["{taxid}", "{classes}", "{g}", ["{g}"] ],')
        #  [ "573", "CEPHALOSPORIN", "blaNDM-1",  [ "blaNDM-1" ] ]      
