#!/bin/bash
#SBATCH --job-name=nextflow_job
#SBATCH --partition=short,long
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=8:00:00
#SBATCH --output=nextflow.out
#SBATCH --error=nextflow.err

pipeline_path=/well/aanensen/shared/nextflow_workflows/amrfinder-review/

module load Java/17.0.4
# Run Nextflow
$pipeline_path/nextflow run $pipeline_path/main.nf -profile bmrc --index $pipeline_path/testing_results/full_samplesheet_fasta.csv --outdir testing_results