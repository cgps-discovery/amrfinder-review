FROM ncbi/amr:3.10.23-2021-12-21.1


RUN apt update && \
    apt install -y -q --no-install-recommends git gcc wget && \
    apt clean && \ 
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install -y -q --no-install-recommends python3-pip  python3-dev && \
    pip3 install requests py-fasta-validator  boto3 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -m ftp://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/3.10/2021-12-21.1/ && \
    mv ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/3.10/2021-12-21.1 /


ARG STDLIB_VERSION=v0.0.13
ENV STDLIB_VERSION ${STDLIB_VERSION}
RUN git clone --depth 1 --branch ${STDLIB_VERSION} https://github.com/cgps-discovery/discovery_stdlib.git && \
    mkdir /amrfinder && \
    mv /data/discovery_stdlib /amrfinder/.


ADD DRR021826.fasta /DRR021826.fasta
ADD DRR031245.fasta /DRR031245.fasta


ADD entrypoint.py /amrfinder/
ADD amrfinder_taxid.py /amrfinder/
WORKDIR /amrfinder


ENTRYPOINT ["python3","entrypoint.py"]