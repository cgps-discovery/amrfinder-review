#!/usr/bin/python3

from discovery_stdlib.util import printer, dict_to_gzjson, get_upload_path
from discovery_stdlib.do_lib import upload_s3
from discovery_stdlib.local_lib import evaluate_fasta_input
from discovery_stdlib.text import jsongz_extension

import os
import sys
import subprocess
from argparse import ArgumentParser
import amrfinder_taxid


TASK = "amrfinder"
GET_VERSION_CMD = 'amrfinder --version'
RUN_SPOTYPING_CMD = 'quast.py %s -o %s'
RUN_SPOTYPING_CMD = 'amrfinder  --plus -d /2021-12-21.1 -n %s -o %s'
TASK_OUTPUT_FILE = "amrfinder.tsv"


def get_amrfinder_version(is_verbose):
    """
    Runs AMRFinder
    :param reference_dir: local path to fasta_file
    :param working_dir: working directory
    :return: path to simple AMRFinder results
    """
    
    if is_verbose: printer('Getting AMRfinder version')
        
    cmd = GET_VERSION_CMD
    if is_verbose: printer("Running: %s" % cmd)
    
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text, err = p.communicate()

    return text.decode("utf-8").strip().split(" ")[-1]


def run_amrfinder(fasta_path, working_dir, is_verbose, is_debug, organism=None):
    """
    Runs Spotyping
    :param reference_dir: local path to fasta_file
    :param working_dir: working directory
    :return: path to simple AMRFinder results
    """
    

    if is_verbose: printer('Running Spotyping')

    if organism is not None:
        cmd = RUN_SPOTYPING_CMD % (fasta_path, os.path.join(working_dir, TASK_OUTPUT_FILE))+ " -O %s" % (organism)
    else:
        cmd = RUN_SPOTYPING_CMD % (fasta_path, os.path.join(working_dir, TASK_OUTPUT_FILE))
    
    if is_verbose: printer("Running: %s" % cmd)

    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text, err = p.communicate()

    if is_debug:
        if text is not None:
            print(*("\t"+x for x in text.decode("utf-8").strip().split("\n")),sep="\n", file=sys.stderr)
        if err is not None:
            print(*("\t"+x for x in err.decode("utf-8").strip().split("\n")),sep="\n", file=sys.stderr)
    
    return os.path.join(working_dir, TASK_OUTPUT_FILE)


def parse_output(amrfinder_result_path, working_dir, is_verbose):
    """
    Captures the essential output from Quast
    :param quast_result_path:
    :working_dir:
    :return:
    """

    if is_verbose: printer('Parsing results')
    
    try:

        result_file = open(amrfinder_result_path, 'r')
        result_lines = [x.strip() for x in result_file]
        result_file.close()

        mod_list = []
        for i in range(1, len(result_lines)):  # Skip the first item
            info = result_lines[i].split("\t")
            print(result_lines[i])
            mod_list.append( {'protein_identifier': info[0], 'contig_id': info[1], 'start': info[2], 'stop': info[3], 'strand': info[4], 'gene_symbol': info[5],'sequence_name': info[6], 'scope': info[7], 'element_type': info[8], 'element_subtype': info[9], 'class': info[10], 'subclass': info[11], 'method': info[12], 'target_length': info[13], 'ref_seq_length': info[14], 'percent_cov_of_ref_seq': info[15], 'percent_id_to_ref_seq': info[16], 'alignment_length': info[17], 'acc_of_closest_sequence': info[18], 'name_of_closest_sequence': info[19], 'hmm_id': info[20], 'hmm_description': info[21]} )
        result = "[" + ",".join([str(x) for x in mod_list]) + "]"   
    except Exception as e:
        result = ""
        return e

    return result

        
def main():
    stdlib_version = os.environ['STDLIB_VERSION'] if (os.environ['STDLIB_VERSION'] != None) else "-"

    argparser = ArgumentParser()
    
    argparser.add_argument('--fasta_s3_path', type=str, help='Fasta assembly s3 path')
    argparser.add_argument('--tax_id', type=str, help='tax id of the genome')
    argparser.add_argument('--output_s3_path', type=str, help='Output s3 path', required=True)
    argparser.add_argument('--id', type=str, help='label of the genome')
    argparser.add_argument('--working_dir', type=str, default='/tmp')
    argparser.add_argument('--verbose', action='store_true')
    argparser.add_argument('--debug', action='store_true')
    
    args = argparser.parse_args()
    if args.fasta_s3_path is None and not sys.stdin.isatty:
        argparser.error("if --fasta_s3_path is not set, this code requires the fasta as stdin.")
    
    # Evaluate input file
    fileid, fasta_path = evaluate_fasta_input(args.fasta_s3_path, args.working_dir, args.verbose)
    # Get SpoTyping version
    amrfinder_version = get_amrfinder_version(args.verbose)
    #Get organims
    organism = amrfinder_taxid.info[args.tax_id]
    # Runs SpoTyping
    amrfinder_results_path = run_amrfinder(fasta_path, args.working_dir, args.verbose, args.debug, organism=organism)
    # Parses SpoTyping output
    parsed_amrfinder_json = parse_output(amrfinder_results_path, args.working_dir, args.verbose)
    # Final Output
    result = {'fileId':fileid,'task':TASK,'version':amrfinder_version,'stdlib_version':stdlib_version,'results':parsed_amrfinder_json}
    # Print results
    print( str(result) )
    # Save as gzipped json
    gzjson_result = dict_to_gzjson(result,args.working_dir,args.verbose)
    # Upload result to digital ocean
    upload_s3( get_upload_path(args.output_s3_path,fileid,jsongz_extension), gzjson_result, "application/json",args.verbose)

if __name__ == '__main__':
    main()