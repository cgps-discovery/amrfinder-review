#!/usr/bin/env bash
set -e

#tar -c DRR031245.fasta taxid.txt > test.tar
cat - | tar -x -C /tmp

TAXO=$(python3 $PWD/convert_taxid.py /tmp/taxid.txt)
#/opt/amrfinder/amrfinder  --plus -d /2021-12-21.1 -n /tmp/sequence.fa -o amrfinder_output.tsv -O ${TAXO}

if [ "$TAXO" = "None" ]; then
    /opt/amrfinder/amrfinder  --plus -d /2021-12-21.1 -n /tmp/sequence.fasta -o amrfinder_output.tsv
else
    /opt/amrfinder/amrfinder  --plus -d /2021-12-21.1 -n /tmp/sequence.fasta -o amrfinder_output.tsv -O ${TAXO}
fi

python3 $PWD/convert_output.py amrfinder_output.tsv