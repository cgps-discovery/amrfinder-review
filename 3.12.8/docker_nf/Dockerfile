FROM --platform=linux/x86_64 python:3.7-slim AS base

LABEL authors="julio.diaz@cgps.group"

RUN apt update && \
    apt install -y -q --no-install-recommends git curl ca-certificates gcc hmmer libcurl4 wget procps && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

# Fetch legacy database 
RUN cd / && wget -m https://quadram-bioinfo-amrfinder.s3.climb.ac.uk/amrfinderdb.2021-12-21.1.tar.gz -O amrfinderdb.2021-12-21.1.tar.gz \
    && tar -xvzf amrfinderdb.2021-12-21.1.tar.gz  && mv 2021-12-21.1/ /opt/

# # INSTALL BLAST VERSION TO MATCH BMRC
ARG BLAST_VERSION=2.12.0
ENV BLAST_VERSION ${BLAST_VERSION}

RUN wget https://quadram-bioinfo-amrfinder.s3.climb.ac.uk/ncbi-blast-${BLAST_VERSION}.tar.gz -O ncbi-blast.tar.gz && tar -xvzf ncbi-blast.tar.gz && mkdir /opt/blast \ 
    && mv tmp/blast/ /opt/ && rm ncbi-blast.tar.gz

RUN mkdir amrfinder && \
    cd amrfinder && \
    wget https://github.com/ncbi/amr/releases/download/amrfinder_v3.10.23/amrfinder_binaries_v3.10.23.tar.gz && \
    tar -xzf amrfinder_binaries_v3.10.23.tar.gz && \
    rm amrfinder_binaries_v3.10.23.tar.gz && \
    cd .. && \
    mv amrfinder /opt/

ENV PATH="/opt/amrfinder/:/opt/blast/bin:${PATH}" 
ENV AMRFINDER_DB=/opt/2021-12-21.1
ENV BLAST_BIN=/opt/blast/bin

FROM --platform=linux/x86_64 base as aws

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

ADD entrypoint.py /amrfinder/
ADD amrfinder_taxid.py /amrfinder/
WORKDIR /amrfinder

ENTRYPOINT ["python3","entrypoint.py"]

FROM --platform=linux/x86_64 base as runtime

ADD run.py /amrfinder/
WORKDIR /amrfinder
RUN mkdir /amrfinder/temp

CMD ["python3","/amrfinder/run.py"]
