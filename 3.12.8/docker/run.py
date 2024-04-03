import subprocess
import json
import sys
import random 
import string
import argparse
import csv
import json 
import argparse
import os 
import ast
from itertools import groupby


# Available --organism options: Acinetobacter_baumannii, Campylobacter, 
# Clostridioides_difficile, Enterococcus_faecalis, Enterococcus_faecium, 
# Escherichia, Klebsiella, Neisseria, Pseudomonas_aeruginosa, Salmonella, 
# Staphylococcus_aureus, Staphylococcus_pseudintermedius, Streptococcus_agalactiae, 
# Streptococcus_pneumoniae, Streptococcus_pyogenes, Vibrio_cholerae

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
'1313':'Streptococcus_pneumoniae',
'620':'Escherichia', #shigella
'623':'Escherichia', #shigella_flexneri
'624':'Escherichia', #shigella_sonnei
'666': 'Vibrio_cholerae',
None:None
}

tax_id_mapping = {
    '195':'194',    # campylobacter_coli to Campy genus
    '197':'194',    # campylobacter_jejuni to Campy genus
    '149539':'590', # salmonella_enteritidis to Salmonella genus 
    '90370': '590', # styphi to Salmonella genus 
    '90371': '590', # salmonella_typhimurium to Salmonella genus 
    '623':'620',    # shigella_flexneri to shigella id
    '624':'620',    # shigella_sonnei to shigella id
}

rename = {
    '485' : [
                ('QUINOLONE','FLUOROQUINOLONE'),
                ('AZITHROMYCIN/CEPHALOSPORIN/TETRACYCLINE','CEPHALOSPORIN')
            ]
}

banned_methods = [
    "PARTIALX",
    "PARTIALP",
    "PARTIAL_CONTIG_ENDX",
    "PARTIAL_CONTIG_ENDP",
    "INTERNAL_STOP",
]

def evaluate_subclass(subclass, tax_id):
    """
    Evaluates the subclass and tax_id to determine if the subclass should be renamed
    :param subclass: The subclass to evaluate
    :param tax_id: The tax_id to evaluate
    """
    if tax_id in rename:
        rename_list = rename[tax_id]
        for r in rename_list:
            if subclass == r[0]:
                subclass = r[1]
        
    return subclass

def get_random_string(length=10):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def filter_amr_elements(lst):
    filtered = []
    for item in lst:
        if item["element_type"] == "AMR" and item["method"] not in banned_methods:
            filtered.append(item)

    return filtered

def group_by_subclass(lst):
    # Sort the list by the 'subclass' key
    sorted_list = sorted(lst, key=lambda x: x['subclass'])
    
    # Group the list by the 'subclass' key
    groups = {k: list(g) for k, g in groupby(sorted_list, key=lambda x: x['subclass'])}

    return groups


def extract_genes_from_groups(groups):
    output = {}
    for key, lst in groups.items():
        output[key] = {}
        for item in lst:
            output[key][item["gene_symbol"]] = True

    return output

def get_curated_mechanisms(organism, curated_mechanisms):
    rules = []
    for tax_id, subclass, gene, mechanisms in curated_mechanisms:
        if tax_id == organism:
            rules.append({'subclass': subclass, 'gene': gene, 'mechanisms': mechanisms})

    if len(rules) > 0:
        return rules
    else:
        raise ValueError(f'Invalid organism code {organism}')
    

def parse_subclass(subclass):
    """
    This function checks if string can be converted to a list, and if so, it returns the list
    otherwise it returns the string
    :param subclass: The subclass to evaluate
    """
    try:
        subclass = ast.literal_eval()
    except:
        subclass = subclass
    return subclass        

def generate_curated_output(curated_mechanisms, result_list, tax_id): 
    amr_elements = filter_amr_elements(result_list)
    groups = group_by_subclass(amr_elements)
    if tax_id in ['354276', '573', '562'] and groups.get('CARBAPENEM'):
        if groups.get('CEPHALOSPORIN'):
            groups['CEPHALOSPORIN'] += groups['CARBAPENEM']
        else:
            groups['CEPHALOSPORIN'] = groups['CARBAPENEM']
    if tax_id in ['573'] and groups.get('CEPHALOSPORIN'):    
        if groups.get('CARBAPENEM'):
            groups['CARBAPENEM'] += groups['CEPHALOSPORIN']
        else:
            groups['CARBAPENEM'] = groups['CEPHALOSPORIN']        
    if tax_id in ['727'] and groups.get('CEPHALOSPORIN'):
        if groups.get('BETA-LACTAM'):
            groups['BETA-LACTAM'] += groups['CEPHALOSPORIN']
        else:
            groups['BETA-LACTAM'] = groups['CEPHALOSPORIN']    

    hits_by_subclass = extract_genes_from_groups(groups)

    output = {}
    found_hits = dict()
    rules = get_curated_mechanisms(tax_id, curated_mechanisms)
    for rule in rules:
        subclasses, gene, mechanisms = parse_subclass(rule['subclass']), rule['gene'], rule['mechanisms']
        if isinstance(subclasses, list):
            for subclass in subclasses:
                temp_found_hits = hits_by_subclass.get(subclass)
                if temp_found_hits is not None:
                    found_hits.update(temp_found_hits)
                subclass = subclasses[0]
        else:
            subclass = subclasses
            found_hits = hits_by_subclass.get(subclass)
        if found_hits:
            if all(x in found_hits for x in mechanisms):
                if subclass not in output:
                    output[subclass] = set()
                for item in gene.split(";"):
                    output[subclass].add(item)

    for subclass, set_ in output.items():
        output[subclass] = sorted(list(set_))
    return output, found_hits

def apply_filters(result, tax_id, curated_file):
    curated_mechanisms = json.load(open(curated_file))
    TAX_IDS = list(set([x[0] for x in curated_mechanisms]))
    if tax_id in TAX_IDS:
        output, found_hits = generate_curated_output(curated_mechanisms, result, tax_id)
        return output
    else:
        return None 

def parse_output(result_lines, tax_id, curated_file, curated=False):
    """
    Captures the essential output from Quast
    :param quast_result_path: Path to the AMRFinder output file
    :param tax_id: The tax_id to evaluate
    """
    mod_list = []
    for line in result_lines[1:]:  # Skip the first item
        info = line.split("\t")
        if len(info) > 21:
            info[11] = evaluate_subclass(info[11], tax_id)
            data = {"protein_identifier": info[0], "contig_id": info[1], "start": info[2], "stop": info[3], "strand": info[4], "gene_symbol": info[5],"sequence_name": info[6], "scope": info[7], "element_type": info[8], "element_subtype": info[9], "class": info[10], "subclass": info[11], "method": info[12], "target_length": info[13], "ref_seq_length": info[14], "percent_cov_of_ref_seq": info[15], "percent_id_to_ref_seq": info[16], 'alignment_length': info[17], "acc_of_closest_sequence": info[18], "name_of_closest_sequence": info[19], "hmm_id": info[20], "hmm_description": info[21]}
            mod_list.append( data )        
    result = json.dumps(mod_list) 
    if curated: 
        json_ready = json.loads(result)
        result = json.dumps(apply_filters(json_ready, tax_id, curated_file))
        if result == 'null':
            print('Error; no curated rules found' , file=sys.stderr)
    return result

def main(args):
    file_name = get_random_string()

    input_file_path = f'{args.tempdir}/{file_name}.fasta'
    output_file_path = f'{args.tempdir}/{file_name}_output.tsv'

    in_file = open(input_file_path, 'w')
    lines_of_data = sys.stdin.read() 
    if not lines_of_data:
        print('No input data received', file=sys.stderr)
        print('If this is Docker did you remember to use --interactive?', file=sys.stderr)
        sys.exit(1)
    in_file.write(''.join(lines_of_data))
    in_file.close()

    tax_id = tax_id_mapping.get(args.tax_id, args.tax_id)
    organism = database_info.get(tax_id, None)
    if args.existing:
        amrfinder_results = lines_of_data.split('\n')
    else: 
        # Run amrfinder command
        if organism:
            amrfinder_output = subprocess.run(['amrfinder', '--plus', '-n', input_file_path, '-o',output_file_path, '-O', organism], capture_output=True)
        else:
            amrfinder_output = subprocess.run(['amrfinder', '--plus', '-n', input_file_path, '-o', output_file_path], capture_output=True)
        result_file = open(output_file_path, 'r')
        amrfinder_results = [x.strip() for x in result_file]
        result_file.close()

    if args.rawtable:
        print('\n'.join(amrfinder_results))
    else:
        print(parse_output(amrfinder_results, tax_id,  args.curated_file, args.curated))

if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('--tax-id', help='Taxonomy ID', type=str, required=True) 
    parser.add_argument('--curated', help='Show curated results', action='store_true', required=False) 
    parser.add_argument('--curated_file', help='curated_mechanisms json path', type=str, default='curated_mechanisms.json') 
    parser.add_argument('--existing', help='STDIN is an existing amrfinder output table (usually fasta)', action='store_true', required=False) 
    parser.add_argument('--rawtable', help='Show original arfinder output table', action='store_true', required=False) 
    parser.add_argument('--tempdir', help='Change tempdir default is /amrfinder/temp/', type=str, default='/amrfinder/temp/') 

    args = parser.parse_args()
    main(args)
