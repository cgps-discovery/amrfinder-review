FROM --platform=linux/x86_64 python:3.7-slim AS base

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

FROM --platform=linux/x86_64 base as runtime

LABEL base.image="python:3.7-slim"
LABEL software="AMRFinderPlus"
LABEL software.version="3.12.8"
LABEL description="AMR"
LABEL website="https://github.com/cgps-discovery/amrfinder-review"
LABEL license="https://github.com/cgps-discovery/amrfinder-review/blob/MAIN/LICENSE"
LABEL maintainer="Nabil-Fareed Alikhan + Julio Diaz Caballero" 
LABEL maintainer.email="julio.diaz@cgps.group"

ADD curated_mechanisms.json /amrfinder/
ADD run.py /amrfinder/

WORKDIR /amrfinder
RUN mkdir /amrfinder/temp

ENTRYPOINT ["python3","/amrfinder/run.py"]

FROM --platform=linux/x86_64 base as nextflow

ADD run.py /amrfinder/
ADD curated_mechanisms.json /amrfinder/
WORKDIR /amrfinder
RUN mkdir /amrfinder/temp

CMD ["python3","/amrfinder/run.py"]
