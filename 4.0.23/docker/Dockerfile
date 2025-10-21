# Use a specific micromamba image as the base
FROM --platform=linux/x86_64 mambaorg/micromamba:latest AS base

# Avoid lock issues
ENV MAMBA_NO_LOCKS=1
# Put conda environment into /opt/conda
ENV CONDA_DIR=/opt/conda
ENV PATH="${CONDA_DIR}/bin:${PATH}"

# Install AMRFinderPlus and Python into /opt/conda (clean caches after)
RUN micromamba install -y -p ${CONDA_DIR} -c conda-forge -c bioconda \
        ncbi-amrfinderplus python=3.11 \
    && micromamba clean --all --yes || true

# Make sure we have download tools available in the base image so we can fetch the AMRFinder DB
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Set the AMRFINDER_DB location inside the image and download the DB at build-time so it's embedded
ENV AMRFINDER_DB=/opt/conda/share/amrfinderplus/data/latest
RUN /opt/conda/bin/amrfinder -u || (echo "amrfinder -u failed" && false)
USER 1000

# -------------------------
# Runtime image (minimal tweaks / labels)
# -------------------------
FROM base AS runtime

LABEL base.image="mambaorg/micromamba:1.4.9-debian-slim"
LABEL software="AMRFinderPlus"
LABEL software.version="4.0.23"
LABEL description="AMR"
LABEL website="https://github.com/cgps-discovery/amrfinder-review"
LABEL license="https://github.com/cgps-discovery/amrfinder-review/blob/MAIN/LICENSE"
LABEL maintainer="Nabil-Fareed Alikhan"
LABEL maintainer.email="nabil.alikhan@cgps.group"

USER root

# Create application directory and make it writable if needed
RUN mkdir -p /opt/amrfinder /opt/amrfinder/temp && chmod -R 0775 /opt/amrfinder

# Copy app files
COPY curated_mechanisms.json /opt/amrfinder/
COPY run.py /opt/amrfinder/

WORKDIR /opt/amrfinder

# Add a small entrypoint wrapper that forwards all args to the python runner.
# This avoids micromamba's wrapper interpreting arguments starting with `--`.
RUN printf '%s\n' "#!/bin/sh" "exec /opt/conda/bin/python /opt/amrfinder/run.py \"\$@\"" > /usr/local/bin/amrfinder-entrypoint.sh \
    && chmod +x /usr/local/bin/amrfinder-entrypoint.sh

# Use the local wrapper as entrypoint so `docker run image --tax-id 562` works
ENTRYPOINT ["/usr/local/bin/amrfinder-entrypoint.sh"]

# -------------------------
# Alternate stage for nextflow (if you want a separate image target)
# -------------------------
FROM base AS nextflow

USER root
RUN mkdir -p /opt/amrfinder /opt/amrfinder/temp && chmod -R 0775 /opt/amrfinder

COPY curated_mechanisms.json /opt/amrfinder/
COPY run.py /opt/amrfinder/

WORKDIR /opt/amrfinder

# For nextflow target use the same wrapper
CMD ["/usr/local/bin/amrfinder-entrypoint.sh"]
