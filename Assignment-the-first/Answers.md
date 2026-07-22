# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz |  |  |  |
| 1294_S1_L008_R2_001.fastq.gz |  |  |  |
| 1294_S1_L008_R3_001.fastq.gz |  |  |  |
| 1294_S1_L008_R4_001.fastq.gz |  |  |  |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. **YOUR ANSWER HERE**
    3. **YOUR ANSWER HERE**
    
## Part 2
1. Define the problem

We have been given 4 fastq files. The R1 and R4 files have biological data (reads that were sequenced). The R2 and R3 files have indexes or barcodes which were attached to the reads to differentiate between them since they all came from a single flow cell. 

The R1 file contains the reads from the first strand.

The R2 file contains the index 1s (read from the first strand).

The R3 file contians the index 2s (read from the second strand on the opposite end of index 1).

The R4 file contains the second strand reads.

This is paired-end sequencing data, so every read from R1 should have an identical beginning of its header in a read from R4. 

Index 1 and Index 2 are not the same sequence. If library prep and sequencing happened correctly both ends of the strands attached would have been the same, so index 1 and index 2 should be reverse complements of each other. We call this situation dual-matching indexes. 

Another situation that could happen is if there is index hopping, which would mean the ends of the DNA are not the same, and index 1 and index 2 are not reverse complements of each other. There are two possibilites from this situation: 1. both indexes could be known indexes and just not matching. 2. one or both of the indexes could be unkown.

The third situation that could happen is that the indexes match, but they are not a known index sequence.

Our job is to look at each index pair, correctly categorize it, and output the correct format of fastq files given which situation the index pair falls under. We also have to keep track of the number of index pairs in each situation.



2. Describe output

If:
1. One of the indexes is too low quality (below the threshold we decide)
Then we add each of the paired reads to the 2 fastq files that hold all the reads with unknown indexes, R1 having the read associated with index 1 (so from the input R1 fastq file), and R2 having the read associated with index 2 (so from the input R4 fastq file). Both the output fastq files would have the indexes appended to their header lines
AND we add one to our tally of unknown index pairs

If:
1. one of the indexes has an N in its sequence
Then we add each of the paired reads to the 2 fastq files that hold all the reads with unknown indexes, R1 having the read associated with index 1 (so from the input R1 fastq file), and R2 having the read associated with index 2 (so from the input R4 fastq file). Both the output fastq files would have the indexes appended to their header lines, which would look something like this: NNNNNNNG-CGATTAGC
AND we add one to our tally of unknown index pairs


If: 
2. neither of the indexes matches the sequence of one of the 24 sequences in our library of known indexes
Then we add each of the paired reads to the 2 fastq files that hold all the reads with unknown indexes, R1 having the read associated with index 1 (so from the input R1 fastq file), and R2 having the read associated with index 2 (so from the input R4 fastq file). Both the output fastq files would have the indexes appended to their header lines, which would look something like this: CCCCCCCC-CCCCCCCC
AND we add one to our tally of unknown index pairs

If:
2. one of the indexes matches the sequence of one of the 24 sequences in our library of known indexes
3. the indexes are reverse complements of each other meaning the ends of the DNA were the same
Then we output 2 fastq files, R1 having the read associated with index 1 from the first strand (so from the input R1 fastq file), and R2 having the read associated with index 2 from the second strand (so from the input R4 fastq file). Both the output fastq files would have the indexes appended to their header lines, which would look something like this: GTAGCGTA-TACGCTAC.
AND we add one to our tally of dual-matching index pairs


If:
2. one of the indexes matches the sequence of one of the 24 sequences in our library of known indexes
3. the other index matches the sequence of a different sequence in our library of known indexes
Then we add each of the paired reads to the 2 fastq files that hold all the reads with index hopping, R1 having the read associated with index 1 from the first strand (so from the input R1 fastq file), and R2 having the read associated with index 2 from the second strand (so from the input R4 fastq file). Both the output fastq files would have the indexes appended to their header lines, which would look something like this: GTAGCGTA-CCCCCCCC
AND we add one to our tally of index-hopping index pairs

Either print or write the tallies to a file


5. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
6. Pseudocode


If both indexes are reverse complements, then they are matching. We would check to see if one of them matches an index from our library of 24 known indexes.


If both indexes are known, we check to see if they are matching.


If both indexes are matching, we output two fastq files, one with the R1 read associated and the index attached to the header, and one with the R4 read associated and the (identical) index attached to the header.



Example: index 1 is GTAGCGTA which matches the B1 index and thus is known, and index 2 is also GTAGCGTA.

Our R1 fastq file would have the read from the R1 input fasta file, and its header would have the index GTAGCGTA-GTAGCGTA appended to the end.

Our R2 fastq file would have the read from the R4 input fasta file, and its header would have the index GTAGCGTA-GTAGCGTA appended to the end.



If both indexes are not matching, we output two fastq files, one with the R1 read associated and the index attached to the header, and one with the R4 read associated and the (not identical) index attached to the header.


If the index pair is not matching, we then look at if both indexes are known or not. 

If one or both of the indexes are not known, 

If sequencing went correctly, a read from R1 and its corresponding read from R4 


6. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
