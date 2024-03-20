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
