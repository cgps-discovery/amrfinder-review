from os.path import basename, splitext, isfile, join
import pandas as pd
from datetime import datetime
from os import listdir
import argparse
import sys 

def now():
  now = datetime.now()
  return now.strftime("%Y-%m-%d %H:%M:%S")

BANNED_METHOD = ["PARTIALX", "PARTIALP", "PARTIAL_CONTIG_ENDX", "PARTIAL_CONTIG_ENDP", "INTERNAL_STOP"]

def main(args):
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m AMRFinder Gathering script.")

    # Directory containing all AMRDinder results
    INPUT_DIR = args.INPUT_DIR
    # Output file of long form
    LONG_OUT = args.LONG_OUT
    # Output file of simplified form
    SIMPLE_OUT = args.SIMPLE_OUT

    # List of files in that directory
    file_names = [f for f in listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f)) and f.endswith('.txt')]

    # Create dataframe from each AMRFinder result
    frames = []
    in_list = []
    for in_file in file_names:
        df = pd.read_csv(INPUT_DIR+"/"+in_file, sep="\t")
        # Choose only rows with AMR in 'Element type' (acquired resistance)
        df = df[df["Element type"] == "AMR"]

        # Add name of isolate ('run_accession') to dataframe
        name = splitext(splitext(basename(in_file))[0])[0]
        in_list.append(name)
        df["accession_id"] = name

        frames.append(df)
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m Loaded "+str(len(frames))+" AMRFinder results.", file=sys.stderr)
   
    # Join all dataframes in a big one
    result = pd.concat(frames)


    cols = list(result.columns)
    cols = [cols[-1]] + cols[:-1]
    result = result[cols]
    result.to_csv(LONG_OUT, index=False)
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m Concatenated AMRFinder results.",  file=sys.stderr)

    # Remove partial hits
    result = result[~result.Method.isin(BANNED_METHOD)]
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m Partial hits removed.",  file=sys.stderr)


    # Print out antibiotics tree
    class_u = result["Class"].unique()
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m Loaded "+str(len(class_u))+" ABX subclasses.",  file=sys.stderr)

    # Get list of Subclasses of antibiotics
    subclasses = result["Subclass"].unique()
    # Get list of accession ids
    ids = list(result["accession_id"].unique())


    # Crate list of headers including all subclasses in dataset
    header_list = []
    header_list.append("accession_id")
    for subclass in subclasses:
        header_list.append(subclass)

    df_array = []
    # For each accession id in dataframe
    for row in ids:
        t = []
        t.append(row)
        
        # Get slice of table corresponding to that accession_id
        temp = result[result["accession_id"]==row]
        # For each subclass in dataframe
        for subclass in subclasses:
            # Get slice of table for each subclass 
            sub_temp = temp[temp["Subclass"]==subclass]
            # If the table is empty, the accession_id doesnt carry a gene 
            # associated with the current subclass.
            if len(sub_temp) == 0:
                t.append("none")
            else:
                gene = list(sub_temp["Gene symbol"])
                gene.sort()
                t.append(";".join(gene))
        df_array.append(t)
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m AMRFinder results simplified.",  file=sys.stderr)

    # get list of ids in `df_array``
    temp_list = [i[0] for i in df_array]
    # see which ones are missing from the list of files
    missing = list(set(in_list)-set(temp_list))
    #add row to `df_array` with nones
    for m in missing:
        placeholder =["none"]*len(header_list)
        placeholder[0] = m
        df_array.append(placeholder)
    if args.verbose:        
        print("\033[92m \033[1m "+now()+" \033[0m Empty results reviewed.",  file=sys.stderr)


    final_df = pd.DataFrame(df_array, columns = header_list)
    final_df.to_csv(SIMPLE_OUT, index=False)
    if args.verbose:
        print("\033[92m \033[1m "+now()+" \033[0m Simple Format Printed.",  file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('INPUT_DIR', type=str, help='Input directory')
    parser.add_argument('LONG_OUT', type=str, help='Long output file')
    parser.add_argument('SIMPLE_OUT', type=str, help='Simple output file')

    args = parser.parse_args()
    main(args)
