# Docker container for amrfinder

## Build locally and run 

```bash
docker build -t amrfinder --target runtime 3.12.8/docker_nf && docker run -i  amrfinder < test_ass/ERR4626366.fasta --tax-id 1280
```

## 



## USAGE

This container takes up to two files passed as stdout of tar.

1. `sequence.fasta` is the input assembly file in fasta format
2. `taxid.txt` a text file containing only the texonomic id of the input genome (optional)

These two files should be passed to docker using `tar -c`. The docker container would untar these files.

### Example 1

The taxonomic id is not known or species is not supported by amrfinder

```bash
tar -c sequence.fasta | docker run -i docker.io/juliofdiaz/amrfinder:beta
```

### Example 1

The taxonomic id is recorded in the `texid.txt` file

```bash
tar -c sequence.fasta taxid.txt | docker run -i docker.io/juliofdiaz/amrfinder:beta
```

## TO DO

* Push to ECR