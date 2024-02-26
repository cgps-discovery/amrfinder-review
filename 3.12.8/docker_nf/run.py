import subprocess
import json
import sys
import random 
import string

# Available --organism options: Acinetobacter_baumannii, Campylobacter, 
# Clostridioides_difficile, Enterococcus_faecalis, Enterococcus_faecium, 
# Escherichia, Klebsiella, Neisseria, Pseudomonas_aeruginosa, Salmonella, 
# Staphylococcus_aureus, Staphylococcus_pseudintermedius, Streptococcus_agalactiae, 
# Streptococcus_pneumoniae, Streptococcus_pyogenes, Vibrio_cholerae

info = {
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
'727': None,
'1313':'Streptococcus_pneumoniae',
'620':'Escherichia', #shigella
'623':'Escherichia', #shigella_flexneri
'624':'Escherichia', #shigella_sonnei
'666': 'Vibrio_cholerae',
None:None
}


def get_random_string(length=10):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def parse_output(amrfinder_result_path):
    """
    Captures the essential output from Quast
    :param quast_result_path: Path to the AMRFinder output file
    """

    try:

        result_file = open(amrfinder_result_path, 'r')
        result_lines = [x.strip() for x in result_file]
        result_file.close()

        mod_list = []
        for i in range(1, len(result_lines)):  # Skip the first item
            info = result_lines[i].split("\t")
            data = {"protein_identifier": info[0], "contig_id": info[1], "start": info[2], "stop": info[3], "strand": info[4], "gene_symbol": info[5],"sequence_name": info[6], "scope": info[7], "element_type": info[8], "element_subtype": info[9], "class": info[10], "subclass": info[11], "method": info[12], "target_length": info[13], "ref_seq_length": info[14], "percent_cov_of_ref_seq": info[15], "percent_id_to_ref_seq": info[16], 'alignment_length': info[17], "acc_of_closest_sequence": info[18], "name_of_closest_sequence": info[19], "hmm_id": info[20], "hmm_description": info[21]}
            mod_list.append( data )        
        result = json.dumps(mod_list) 
    except Exception as e:
        result = ""
        return e

    return result
file_name = get_random_string()
input_file_path = f'/amrfinder/temp/{file_name}.fasta'
output_file_path = f'/amrfinder/temp/{file_name}_output.tsv'

in_file = open(input_file_path, 'w')
lines_of_data = sys.stdin.read() 
if not lines_of_data:
    print('No input data received')
    print('If this is Docker did you remember to use --interactive?')
    sys.exit(1)
in_file.write(''.join(lines_of_data))
in_file.close()

import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('--tax-id', help='Taxonomy ID', type=str, required=False) 
args = parser.parse_args()
tax_id = args.tax_id

organism = info.get(tax_id, None)

# Run amrfinder command
if organism:
    amrfinder_output = subprocess.run(['amrfinder', '--plus', '-n', input_file_path, '-o',output_file_path, '-O', organism], capture_output=True)
else:
    amrfinder_output = subprocess.run(['amrfinder', '--plus', '-n', input_file_path, '-o', output_file_path], capture_output=True)
print(parse_output(output_file_path))

