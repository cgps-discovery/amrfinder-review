#!/usr/bin/python3

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

def convert_taxid(taxid):
    return info[taxid]

def main():
    try:
        with open(sys.argv[1]) as f:
            first_line = f.readline().strip()
        print(convert_taxid(first_line))
    except Exception as e:  
        print("None")

if __name__ == "__main__":
    main()