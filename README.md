# Docker container for amrfinder

This runs a legacy version of amrfinder. Software versions are:

* AMRFINDER 3.10.23
* BLAST: 2.12.0
* AMRFINDER database: 2021-12-21.1 

The database is not exactly the same as the one on the AMRFinderPlus repo. 

This may give different results if you run the latest version. 

## Curated_mechanisms.json 

`curated_mechanisms.json` is a json file that details rules for filtering and adjusting AMRFinder results. The master copy is in the root of this repo. 
As part of deployment it is compied to the docker folder, but this is a copy. You should make all changes to `/curated_mechanisms.json` only. 

The format of the file is a list of lists, e.g.: 

```
    [ "1280", "METHICILLIN", "mecC", ["mecC", "mecR", "mecI"]],
```

* [NCBI Taxonomy ID](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=1280)
* Drug name.
* Value to report as output.
* Detected genes (as a list) required to match this profile. Order does not matter.

## Build locally and run 

The Docker file is set up as a multi-stage build. The correct Dockerfile is in `3.12.8/docker_nf`.  Use `--target` choose the correct stage:

* `build`; this is with amrfinder set up and available on the path. 
* `runtime`: This is with amrfinder set up and available on the path, and the `/amrfinder/run.py` script will handle accepting `fasta` on stdin and return a JSON of the results. 
* `nextflow`: This is with amrfinder set up and available on the path, and the `/amrfinder/run.py` script will handle accepting `fasta` on stdin and return a JSON of the results. 
This uses `CMD` instead of `endpoint` to allow nextflow to specify the path to the run.py script. Nextflow does not seem to work with executable containers. 


If you want an image where you can pipe in the fasta to standard input, build as:

```bash
docker build -t amrfinder-runtime --target runtime 3.12.8/docker
```

To use it:

```bash
docker run --interactive --platform=linux/x86_64 amrfinder-runtime  \
--tax-id 485  \
--curated < testing_basic/SRR11904224.fasta 
```

* `--tax-id` is required for `--curated` output
* if you use the `--curated`  flag you will get the final json with all the filtering and rules aplied (as per `curated_mechanisms.json`)
* without `--curated` (i.e. by default) it runs the json formatted of the original amrfinder table (no filters applied).
* if you specify `--rawtable` you will receive the original amrfinder tsv on stdout instead.
* with `--existing`, you can pipe in an existing amrfinder output table (usually this is the FASTA). This is for debugging purposes, where you already have an AMRFINDER results table
and you want to check the curated results. 
* N.B This is supposed to run through the container. There is a tempdir in the container for the streamed FASTA file, which is `/amrfinder/temp/`. If you are running run.py directly
(i.e. no container), you will need to give another temp dir with `--tempdir`. You may also need to specify the path of `curated_mechanisms.json` as well, so usage would be: 

```bash
mkdir ~/amrfinder_temp
python3 3.12.8/docker/run.py --tax-id 485  \
--curated \
--tempdir ~/amrfinder_temp \
--curated_file 3.12.8/docker/curated_mechanisms.json  < testing_basic/SRR11904224.fasta 
```


# Example 1: I want to run AMRfinder, as is, without any wrapper scripts:

You may want to plug this into nextflow pipelines, or for other development. 

```bash
docker build -t amrfinder --target build 3.12.8/docker
docker run -it -v ${PWD}/test:/data/ amrfinder amrfinder --plus --threads 2 -n testing_basic/SRR11904224.fasta  > SRR11904224_amrfinder.txt 2> SRR11904224_amrfinder.err
# If you know which organism you want: 
docker run -it -v ${PWD}/test:/data/ amrfinder --plus --threads 2  -n testing_basic/SRR11904224.fasta --organism Neisseria > SRR11904224_amrfinder.txt 2> SRR11904224_amrfinder.err
```

# Example 2: I want to run AMRFinder, with FASTA file piped from stdin and a curated JSON output: 

You must specify the tax-id for curated JSON output. 

```bash 
docker build -t amrfinder-runtime --target runtime 3.12.8/docker
docker run --interactive --platform=linux/x86_64 amrfinder-runtime  --tax-id 485  --curated < testing_basic/SRR11904224.fasta 
```
