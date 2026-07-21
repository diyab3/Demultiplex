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

This is paired-end sequencing data, so every read from R1 should have an identical beginning of its header in a read from R4. 

If everything went smoothly, each read will have two identical indexes associated with it, 


2. Describe output
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
