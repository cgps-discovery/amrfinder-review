#!/usr/bin/env nextflow
def versionMessage(){
  log.info """ 

 █████╗ ███╗   ███╗██████╗ ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗     ████████╗███████╗███████╗████████╗
██╔══██╗████╗ ████║██╔══██╗██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
███████║██╔████╔██║██████╔╝█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝       ██║   █████╗  ███████╗   ██║   
██╔══██║██║╚██╔╝██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗       ██║   ██╔══╝  ╚════██║   ██║   
██║  ██║██║ ╚═╝ ██║██║  ██║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║       ██║   ███████╗███████║   ██║   
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝   
                                                                                                              
                                                           
  """
}

// Importing required functions from 'plugin/nf-validation'
include { validateParameters; paramsHelp; paramsSummaryLog; } from 'plugin/nf-validation'

include {   AMRFINDERPLUS1; AMRFINDERPLUS2; AMRFINDERPLUS3;  } from './modules/amrfindr'

// Setting the default value for params.help
params.help = false

// Checking if params.help is true
if (params.help) {
    // Displaying help message using paramsHelp function
    log.info paramsHelp("nextflow main.nf --index sample_data.csv")
    exit 0
}

// Setting the default value for params.index
params.index = "sample_data.csv"

// Validating the parameters
validateParameters()
versionMessage()
// Logging the summary of the parameters
log.info paramsSummaryLog(workflow)

// Defining the workflow
workflow {
    // Creating a channel from the file specified in params.index
    FASTA = Channel.fromPath(params.index) \
        // Splitting the CSV file into rows with headers
        | splitCsv(header:true) \
        // Mapping each row to a tuple with sample and fasta file
        | map { row-> tuple(row.sample, file(row.fasta), row.species, row.taxid) } 

    // Running the AMRFINDER module
    AMRFINDERPLUS1(FASTA) // This is the one we are testing - this produces the base tsv table 
    JSONOUTPUT = AMRFINDERPLUS3(FASTA) // This is the one we are running - this produces the curated json result 
    CHECK_RESULT(JSONOUTPUT, params.index)
}

