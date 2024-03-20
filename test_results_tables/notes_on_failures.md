# Notes accounting for failures in testing 

## pseudomonas_aeruginosa
```
ERR2870085	pseudomonas_aeruginosa	Pseudomonas_aeruginosa	287	CARBAPENEM	blaVIM;blaVIM-2	blaVIM-2	False
```

Raw amrfinder results: 

```
NA      NODE_99_length_1602_cov_5.253493        1164    1601    -       blaVIM  VIM family subclass B1 metallo-beta-lactamase   core    AMR     AMR     BETA-LACTAM     CARBAPENEM      PARTIAL_CONTIG_ENDX     146     266     54.89   100.00  146     WP_013263789.1  subclass B1 metallo-beta-lactamase VIM-1 NA      NA
```

PARTIAL_CONTIG_ENDX is banned. current result is fine, so pseudomonas_aeruginosa is now passing all tests.


## step pneumo
```
SRR7175976	streptococcus_pneumoniae	Streptococcus_pneumoniae	1313	BETA-LACTAM	pbp1a;pbp1a;pbp2x	pbp1a;pbp2x	False
```

Gene is mentioned twice in original. 


## salmonella_typhimurium

```
ERR2202504	salmonella_typhimurium	90371	QUINOLONE	qnrS	none	False
SRR1645142	salmonella_typhimurium	90371	QUINOLONE	oqxB	none	False
SRR10313679	salmonella_typhimurium	90371	QUINOLONE	qnrB;qnrB	none	False
SRR7140623	salmonella_typhimurium	90371	QUINOLONE	qnrS13;qnrVC	qnrS13	False
SRR15242949	salmonella_typhimurium	90371	QUINOLONE	aac(6')-Ib-cr5;qnrS	aac(6')-Ib-cr5	False
SRR16646902	salmonella_typhimurium	90371	QUINOLONE	qnrB	none	False
SRR12354807	salmonella_typhimurium	90371	QUINOLONE	qnrVC;qnrVC	none	False
```

Many of these are due to partial matches, that are ignore in the new results, but mentioned in the original. 

**ERR2202504**

```
NA      NODE_37_length_10146_cov_651.621877     3       494     -       qnrS    QnrS family quinolone resistance pentapeptide repeat protein    core    AMR     AMR     QUINOLONE       QUINOLONE       PARTIAL_CONTIG_ENDX  164     218     75.23   100.00  164     WP_001516695.1  quinolone resistance pentapeptide repeat protein QnrS1  NA      NA
```

**SRR1645142**
```
NA      NODE_57_length_3148_cov_8.082655        75      2483    +       oqxB    multidrug efflux RND transporter permease subunit OqxB  core    AMR     AMR     PHENICOL/QUINOLONE      PHENICOL/QUINOLONE  PARTIALX 803     1050    76.48   100.00  803     WP_000347934.1  multidrug efflux RND transporter permease subunit OqxB  NA      NA
```

**SRR10313679**
```
NA      NODE_28_length_7146_cov_171.455098      2605    3126    +       qnrB    QnrB family quinolone resistance pentapeptide repeat protein    core    AMR     AMR     QUINOLONE       QUINOLONE       PARTIALX     174     214     81.31   100.00  174     WP_012954666.1  quinolone resistance pentapeptide repeat protein QnrB19 NA      NA
NA      NODE_35_length_909_cov_28.503597        368     907     +       qnrB    QnrB family quinolone resistance pentapeptide repeat protein    core    AMR     AMR     QUINOLONE       QUINOLONE       PARTIAL_CONTIG_ENDX  180     214     84.11   100.00  180     WP_012695489.1  quinolone resistance pentapeptide repeat protein QnrB2  NA      NA
```

**SRR12354807**

```
NA      NODE_41_length_4394_cov_275.672841      3       329     -       qnrVC   QnrVC family quinolone resistance pentapeptide repeat protein   core    AMR     AMR     QUINOLONE       QUINOLONE       PARTIAL_CONTIG_ENDX  109     218     50.00   99.08   109     WP_000361705.1  quinolone resistance pentapeptide repeat protein QnrVC5 NA      NA
NA      NODE_41_length_4394_cov_275.672841      3995    4393    -       qnrVC   QnrVC family quinolone resistance pentapeptide repeat protein   core    AMR     AMR     QUINOLONE       QUINOLONE       PARTIAL_CONTIG_ENDX  133     218     61.01   99.25   133     WP_000361704.1  quinolone resistance pentapeptide repeat protein QnrVC4 NA      NA
```