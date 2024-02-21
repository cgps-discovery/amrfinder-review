FROM --platform=linux/x86_64 python:3.7-slim

LABEL authors="julio.diaz@cgps.group"

RUN apt update && \
    apt install -y -q --no-install-recommends git curl ca-certificates gcc hmmer libcurl4 wget && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

# INSTALL BLAST VERSION TO MATCH BMRC
ARG BLAST_VERSION=2.12.0
ENV BLAST_VERSION ${BLAST_VERSION}
RUN echo "Using BLAST version: ${BLAST_VERSION}" && \
    mkdir -p /tmp/blast && \
    mkdir /opt/blast \
    && curl ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/${BLAST_VERSION}/ncbi-blast-${BLAST_VERSION}+-x64-linux.tar.gz | tar -zxC /tmp/blast --strip-components=1 \
    && cd /tmp/blast/bin \
    && mv blastn makeblastdb tblastn /bin/ \
    && cd .. \
    && rm -rf /tmp/blast

# GETTING DATABASE. IT DOESN'T WORK WITH NCBI's COPY
#RUN wget -m ftp://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/3.10/2021-12-21.1/ &&\
#    mv ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/3.10/2021-12-21.1 / && \
#    rm -r ftp.ncbi.nlm.nih.gov
COPY 2021-12-21.1 /2021-12-21.1


RUN mkdir amrfinder && \
    cd amrfinder && \
    wget https://github.com/ncbi/amr/releases/download/amrfinder_v3.10.23/amrfinder_binaries_v3.10.23.tar.gz && \
    tar -xzf amrfinder_binaries_v3.10.23.tar.gz && \
    rm amrfinder_binaries_v3.10.23.tar.gz && \
    cd .. && \
    mv amrfinder /opt/.


RUN apt update && \
    apt install -y -q --no-install-recommends python3-pip python3-dev && \
    pip3 install requests py-fasta-validator boto3 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ARG STDLIB_VERSION=v0.0.13
ENV STDLIB_VERSION ${STDLIB_VERSION}
RUN git clone --depth 1 --branch ${STDLIB_VERSION} https://github.com/cgps-discovery/discovery_stdlib.git && \
    mkdir /amrfinder && \
    mv discovery_stdlib /amrfinder/.

#ADD DRR021826.fasta /DRR021826.fasta
#ADD DRR031245.fasta /DRR031245.fasta

WORKDIR /amrfinder

ENV PATH="/opt/amrfinder/:${PATH}" 

RUN apt update && \
    apt install -y -q --no-install-recommends procps && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*