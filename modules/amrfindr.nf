process AMRFINDERPLUS1 {
    label 'AMRFINDRPLUS_TEST'
    label 'process_low'
    tag {"AMR Prediction $sample"}
    publishDir "${params.outdir}/amrfinder_test", mode: 'copy'

    input:
    tuple val(sample), file(fasta), val(species)

    script:
     if (species =~ /None/){ // Species is not defined
    """
    amrfinder -n $fasta > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
    """
      } else { // files with _1 and _2
    """
    amrfinder -n $fasta --organism $species > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
    """ 
    }    
    output:
    tuple val(sample), file("${sample}_amrfinder.txt"), file("${sample}_amrfinder.err")

    stub:
        """
        touch ${sample}_amrfinder.txt
        touch ${sample}_amrfinder.err
        """

}

process AMRFINDERPLUS2 {
    label 'AMRFINDRPLUS_ORIGINAL'
    label 'process_low'
    tag {"AMR Prediction $sample"}
    publishDir "${params.outdir}/amrfinder_ori", mode: 'copy'

    input:
    tuple val(sample), file(fasta), val(species)

    script:
     if (species =~ /None/){ // Species is not defined
    """
    amrfinder -n $fasta > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
    """
      } else { // files with _1 and _2
    """
    amrfinder -n $fasta --organism $species > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
    """ 
    }    
    output:
    tuple val(sample), file("${sample}_amrfinder.txt"), file("${sample}_amrfinder.err")

    stub:
        """
        touch ${sample}_amrfinder.txt
        touch ${sample}_amrfinder.err
        """

}