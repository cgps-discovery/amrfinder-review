import subprocess
import json
import sys

info = {
'470':'Acinetobacter_baumannii',
'562':'Escherichia',
'354276':'Enterobacter_cloacae',
'573':'Klebsiella_pneumoniae',
'287':'Pseudomonas_aeruginosa',
'194':'Campylobacter',
'1352':'Enterococcus_faecium',
'485':'Neisseria_gonorrhoeae',
'1280':'Staphylococcus_aureus',
'149539':'Salmonella',
'90370':'Salmonella',
'90371':'Salmonella',
'727':None,
'1313':'Streptococcus_pneumoniae',
'620':'Escherichia',
None:None
}



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

in_file = open('/input.fasta', 'w')
lines_of_data = sys.stdin.read() 
if not lines_of_data:
    print('No input data received')
    print('If this is Docker did you remember to use --interative?')
    sys.exit(1)
in_file.write(''.join(lines_of_data))
in_file.close()

import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('--tax-id', help='Taxonomy ID', type=str, required=False) 
args = parser.parse_args()
tax_id = args.tax_id

organism = info[tax_id]

# Run amrfinder command
if organism:
    amrfinder_output = subprocess.run(['amrfinder', '--plus', '-n', '/input.fasta', '-o', 'amrfinder_output.tsv', '-O', organism], capture_output=True)
else:
    amrfinder_output = subprocess.run(['amrfinder', '--plus', '-n', '/input.fasta', '-o', 'amrfinder_output.tsv'], capture_output=True)
print(parse_output('amrfinder_output.tsv'))

