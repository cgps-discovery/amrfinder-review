import csv
import json 
import argparse
import os 
from itertools import groupby

banned_methods = [
    "PARTIALX",
    "PARTIALP",
    "PARTIAL_CONTIG_ENDX",
    "PARTIAL_CONTIG_ENDP",
    "INTERNAL_STOP",
]

TAX_IDS = ['354276', '485', '287', '470', '1280']

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
    
def get_tax_id(accession, filename='species3_sample_data.csv'):
    with open(filename, 'r') as csvfile:
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

def generate_output(curated_mechanisms, result_list, tax_id): 
    amr_elements = filter_amr_elements(result_list)
    groups = group_by_subclass(amr_elements)
    hits_by_subclass = extract_genes_from_groups(groups)
    output = {}
    rules = get_curated_mechanisms(tax_id, curated_mechanisms)
    for rule in rules:
        subclass, gene, mechanisms = rule['subclass'], rule['gene'], rule['mechanisms']
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

def main(args):
    curated_mechanisms = json.load(open(args.curated))
    print('accession', 'species','taxid', 'drug_class', 'expected', 'actual', 'passed', 'found_matches', sep='\t')

    for result_file in [os.path.join(args.file, x) for x in os.listdir(args.file) if x.endswith('.json')]:
        result_list = json.load(open(result_file))
        accession = os.path.basename(result_file).split('_')[0]
        tax_id, species = get_tax_id(accession, args.sample_sheet)
        if tax_id in TAX_IDS:
            original_results = get_real_results(accession, tax_id)
            output, found_hits = generate_output(curated_mechanisms, result_list, tax_id)
            if original_results:
                accession = original_results.pop('accession_id')
                for drug_class, genes in original_results.items():
                    found_matches = ''
                    if found_hits:
                        found_matches = ';'.join(list(found_hits.keys()))
                    if not output.get(drug_class):
                        this_prediction = 'none'
                    else:
                        this_prediction = output.get(drug_class)[0]
                    passed = this_prediction == genes
                    print('accession', 'species','taxid', 'drug_class', 'expected', 'actual', 'passed', 'found_matches', sep='\t')
                    print(accession, species, tax_id, drug_class, genes, this_prediction, passed, found_matches, sep='\t')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', type=str, help='The path to a folder of amrfinder (runtime results)', default='test_amr/amrfinder_run')
    parser.add_argument('--sample_sheet', type=str, help='The path to the samplesheet, with taxids', default='all_sample_data.csv')
    parser.add_argument('--curated', type=str, help='The path curated mechanisms filter as a json', default='curated_mechanisms.json')

    args = parser.parse_args()
    main(args)

            
