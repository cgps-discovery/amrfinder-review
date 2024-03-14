
process CHECK_RESULT {
    label 'CHECK_RESULT'
    label 'process_single'
    tag {"check_result"}

    publishDir "${params.outdir}", mode: 'copy'

    input:
    tuple val(sample), file(fasta), val(species), val(taxid)
    file(index)

    script:
    """
    python3 /amrfinder/run.py --curated_file /amrfinder/curated_mechanisms.json --curated --tax-id $taxid < $fasta > ${sample}_amrfinder.json 2> ${sample}_amrfinder.err
    """

    output:
    tuple val(sample), file("${sample}_amrfinder.json"), file("${sample}_amrfinder.err")

    stub:
        """
        touch ${sample}_amrfinder.json
        touch ${sample}_amrfinder.errs
        """

}