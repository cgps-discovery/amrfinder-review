# Docker container for amrfinder

## Build locally

```bash
docker build --platform linux/amd64 --pull . -t juliofdiaz/amrfinder:alpha
```

## USAGE

## Arguments

* `--fasta_s3_path` : s3 url to fasta assembly
* `--output_s3_path` : s3 url to record results (optional)
* `--working_dir` : working directory (optional)
* `--verbose` : prints progress messages (optional)
* `--debug` : prints everything (optional)
* `--tax_id 287` : NCBI taxonomy id of input genome (optiona)

### Works providing the tax_id, except for E. coli

```bash
docker run --platform linux/amd64 -e SPACES_KEY='${DO_KEY}' -e SPACES_SECRET='${DO_SECRET}' docker.io/juliofdiaz/amrfinder:beta --fasta_s3_path https://pathogenwatch-cgps.ams3.digitaloceanspaces.com/pw-live/fasta/cc/cc172a82d32833a2a6d2068128e57ba0ca91017d.fa.gz --output_s3_path https://cgps.ams3.digitaloceanspaces.com/discovery/analysis/amrfinder/3.12.8/ --working_dir /tmp --verbose --debug --tax_id 287

docker run --platform linux/amd64 -e SPACES_KEY='${DO_KEY}' -e SPACES_SECRET='${DO_SECRET}' docker.io/juliofdiaz/amrfinder:beta --fasta_s3_path https://pathogenwatch-cgps.ams3.digitaloceanspaces.com/pw-live/fasta/70/701745104cd7497d8eabc4389ea412bbecb2bc59.fa.gz --output_s3_path https://cgps.ams3.digitaloceanspaces.com/discovery/analysis/amrfinder/1.0.0/ --working_dir /tmp --verbose --debug --tax_id 470
```

## TO ADDRESS:

- It doesnt work when the tex id is Escherichia.
- When a tax_id is given
- Improve documentation.
