#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --output=demux%j.out
#SBATCH --error=demux%j.err
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=16GB
#SBATCH --job-name=demux

# /usr/bin/time -v python demultiplex.py -R1 ../Assignment-the-first/TEST-input_FASTQ/R1_input.fastq \
#  -R2 ../Assignment-the-first/TEST-input_FASTQ/R2_input.fastq \
#  -R3 ../Assignment-the-first/TEST-input_FASTQ/R3_input.fastq \
#  -R4 ../Assignment-the-first/TEST-input_FASTQ/R4_input.fastq

/usr/bin/time -v python demultiplex.py -R1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
-R2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-R3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
-R4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz