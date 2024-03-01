process AMRFINDERPLUS1 {
    label 'AMRFINDRPLUS_TEST'
    label 'process_single'
    tag {"AMR Prediction test $sample"}
    publishDir "${params.outdir}/amrfinder_test", mode: 'copy'

    input:
    tuple val(sample), file(fasta), val(species)

    script:
     if (species =~ /None/){ // Species is not defined
    """
    amrfinder --plus --threads $task.cpus -n $fasta > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err 
    """
      } else { // files with _1 and _2
    """
    amrfinder --plus --threads $task.cpus  -n $fasta --organism $species > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
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
    label 'process_single'
    tag {"AMR Prediction ori $sample"}

    publishDir "${params.outdir}/amrfinder_ori", mode: 'copy'

    input:
    tuple val(sample), file(fasta), val(species)

    script:
     if (species =~ /None/){ // Species is not defined
    """
    amrfinder --plus --threads $task.cpus  -n $fasta > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
    """
      } else { // files with _1 and _2
    """
    amrfinder --plus --threads $task.cpus -n $fasta --organism $species > ${sample}_amrfinder.txt 2> ${sample}_amrfinder.err
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

process AMRFINDERPLUS3 {
    label 'AMRFINDRPLUS_RUNTIME'
    label 'process_single'
    tag {"AMR Prediction run $sample"}

    publishDir "${params.outdir}/amrfinder_run", mode: 'copy'

    input:
    tuple val(sample), file(fasta), val(species), val(taxid)

    script:
    """
    python3 /amrfinder/run.py --tax-id $taxid < $fasta > ${sample}_amrfinder.json 2> ${sample}_amrfinder.err
    """

    output:
    tuple val(sample), file("${sample}_amrfinder.json"), file("${sample}_amrfinder.err")

    stub:
        """
        touch ${sample}_amrfinder.json
        touch ${sample}_amrfinder.errs
        """

}