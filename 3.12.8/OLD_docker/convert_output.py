#!/usr/bin/python3

import json
import sys

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

def main():
    print(parse_output(sys.argv[1]))

if __name__ == "__main__":
    main()