
process CHECK_RESULT {
    label 'CHECK_RESULT'
    label 'process_single'
    tag {"check_result"}

    input:
    tuple val(sample), path(samplejson), path(sampleerror)
    path(index)

    script:
    """
    check_result.py $index $sample $samplejson  > ${sample}.txt
    """

    output:
    tuple val(sample), file("${sample}.txt")

    stub:
        """
        touch ${sample}.txt
        """

}