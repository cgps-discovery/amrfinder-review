# Docker container for amrfinder

This runs a legacy version of amrfinder. Software versions are:

* AMRFINDER 3.10.23
* BLAST: 2.12.0
* Stdlib: v0.0.13
* AMRFINDER database: 2021-12-21.1 

The database is not exactly the same as the one on the AMRFinderPlus repo. 

This may give different results if you run the latest version. 

## Build locally and run 

The Docker file is set up as a multi-stage build. The correct Dockerfile is in `3.12.8/docker_nf`.  Use `--target` choose the correct stage:

* `build`; this is with amrfinder set up and available on the path. 
* `aws`: This is with the `endpoint.py` as the fixed endpoint. 
* `runtime`: This is with amrfinder set up and available on the path, and the `/amrfinder/run.py` script will handle accepting `fasta` on stdin and return a JSON of the results. There is no errors returns (no stderr)

If you want an image where you can pipe in the fasta to standard input, do:

```bash
docker build -t amrfinder --target runtime 3.12.8/docker_nf
```

The usage is therefore, where `--tax-id` is the NCBI Taxonomic ID:  

```bash
docker run -i  amrfinder < test_ass/ERR4626366.fasta --tax-id 1280
```

# Example 1: I want to run AMRfinder, as is, without any wrapper scripts:

You may want to plug this into nextflow pipelines, or for other development. 

```bash
docker build -t amrfinder --target build 3.12.8/docker_nf 

docker run -it -v ${PWD}/test:/data/ amrfinder amrfinder --plus --threads $cpus -n $fasta_file > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err

# If you know which organism you want: 
docker run -it -v ${PWD}/test:/data/ amrfinder --plus --threads $cpus  -n $fasta_file --organism $species > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
```

# Example 2: I want to run AMRFinder, with stdin and json support:

```bash 
docker build -t amrfinder --target runtime 3.12.8/docker_nf

docker run -i  amrfinder < test_ass/ERR4626366.fasta

# If you know which organism you want: 
docker run -i  amrfinder < test_ass/ERR4626366.fasta --tax-id 1280
```
