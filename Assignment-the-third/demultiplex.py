#!/usr/bin/env python


# Update dictionary counts - DONE
# Output the desired data in a markdown file - DONE
# Incorporate gzip as needed

import argparse
import bioinfo
#import itertools
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="A program to introduce yourself")
    parser.add_argument("-R1", "--R1_input_file", help="Name of the R1 input fasta file", type=str, default="")
    parser.add_argument("-R2", "--R2_input_file", help="Name of the R2 input fasta file", type=str, default="")
    parser.add_argument("-R3", "--R3_input_file", help="Name of the R3 input fasta file", type=str, default="")
    parser.add_argument("-R4", "--R4_input_file", help="Name of the R4 input fasta file", type=str, default="")
    #parser.add_argument("-o", "--output", help="Name of the output file", type=str, default="")
    return parser.parse_args()

args = get_args()

index_file = open("/projects/bgmp/shared/2017_sequencing/indexes.txt", "r")

possible_pairs = {}  # will hold index pairs as keys, and counts as values

indexes = set()  # will hold the index sequences

matched_output_files = {}  # will hold indexes as keys, and lists containing both output files for each index as values

for line_num,line in enumerate(index_file):
    if line_num != 0:
        columns = line.split()
        index_seq = columns[4]
        matched_output_files[index_seq] = [open(f"/scratch/bgmp/diyab/demux/{index_seq}_R1.fq", "w"), open(f"/scratch/bgmp/diyab/demux/{index_seq}_R2.fq", "w")]
        indexes.add(index_seq)
        
index_file.close()

# for perm in itertools.permutations(indexes, r=2):  # creates every possible combination of two known indexes
#     #print(perm)
#     possible_pairs[perm] = 0

for a in indexes:
    for b in indexes:
        possible_pairs[(a,b)] = 0
    
#print(possible_pairs)
    
perfect_matches = 0  # will hold the number of perfect index matches

index_hopped = 0  # will hold the number of index hopped reads

unknown = 0  # will hold the number of reads with unknown indexes

quality_score_threshold = 0  # the cutoff for quality scores

unknown_R1 = open("/scratch/bgmp/diyab/demux/unknown_R1.fq", "w")  # this file will hold all of the forward reads with unknown indexes
unknown_R2 = open("/scratch/bgmp/diyab/demux/unknown_R2.fq", "w")  # this file will hold all of the reverse reads with unknown indexes
index_hopped_R1 = open("/scratch/bgmp/diyab/demux/index_hopped_R1.fq", "w")  # this file will hold all of the forward reads with index hopping
index_hopped_R2 = open("/scratch/bgmp/diyab/demux/index_hopped_R2.fq", "w")  # this file will hold all of the reverse reads with index hopping

# open the input files
input_R1 = open(args.R1_input_file, "rt")
input_R2 = open(args.R2_input_file, "rt")
input_R3 = open(args.R3_input_file, "rt")
input_R4 = open(args.R4_input_file, "rt")

line_num = 0
while True:
        
    # read through the files one line at a time simultaneously
    R1_line = input_R1.readline().strip()  
    R2_line = input_R2.readline().strip()
    R3_line = input_R3.readline().strip()
    R4_line = input_R4.readline().strip()
    
    # HOW TO BREAK OUT OF THE LOOP ONCE WE REACH THE END OF THE FILES
    if R1_line == "":
        break
            
    if line_num % 4 == 0:  # we are on the header line
        R1_header = R1_line
        R2_header = R4_line
    if line_num % 4 == 1:  # we are on the sequence line
        # print(R1_line)
        # print(R2_line)
        # print(R3_line)
        # print(R4_line)
        #print(R3_line)
        R3_index = bioinfo.reverse_complement(R3_line)  # due to how Illumina created the R3 index
        index_pair = f"{R2_line}-{R3_index}"
        
        if "N" in R2_line or "N" in R3_line:  # Unknown read/below quality score threshold
            unknown_R1.write(R1_header)
            unknown_R1.write(f" {index_pair}\n")
            unknown_R2.write(R2_header)
            unknown_R2.write(f" {index_pair}\n")
            unknown_R1.write(f"{R1_line}\n")
            unknown_R2.write(f"{R4_line}\n")
            unknown += 1
        
        else:
            
            if R2_line in indexes:  # R2 index is known
                #print(R2_line)
                if R3_index == R2_line:  # R2 and R3 indexes are perfect matches yay!
                    R1_file = matched_output_files[R2_line][0]
                    R1_file.write(f"{R1_header} {index_pair}\n")
                    R1_file.write(f"{R1_line}\n")
                    R2_file = matched_output_files[R2_line][1]
                    R2_file.write(f"{R2_header} {index_pair}\n")
                    R2_file.write(f"{R4_line}\n")
                    possible_pairs[(R2_line, R3_index)] += 1
                    perfect_matches += 1
                else:  # R2 index is known but R3 index is not a perfect match :(
                    if R3_index in indexes:  # R3 is also known 
                        index_hopped_R1.write(f"{R1_header} {index_pair}\n")
                        index_hopped_R1.write(f"{R1_line}\n")
                        index_hopped_R2.write(f"{R2_header} {index_pair}\n")
                        index_hopped_R2.write(f"{R4_line}\n")
                        possible_pairs[(R2_line, R3_index)] += 1
                        index_hopped += 1
                    else:  # R3 index is unknown
                        #print("writing to unknown")
                        unknown_R1.write(R1_header)
                        unknown_R1.write(f" {index_pair}\n")
                        unknown_R2.write(R2_header)
                        unknown_R2.write(f" {index_pair}\n")
                        unknown_R1.write(f"{R1_line}\n")
                        unknown_R2.write(f"{R4_line}\n")
                        unknown += 1
                        
            else:  # R2 index is unknown
                #print("writing to unknown")
                unknown_R1.write(R1_header)
                unknown_R1.write(f" {index_pair}\n")
                unknown_R2.write(R2_header)
                unknown_R2.write(f" {index_pair}\n")
                unknown_R1.write(f"{R1_line}\n")
                unknown_R2.write(f"{R4_line}\n")
                unknown += 1
            # print(R3_index)
        # elif R2_line not in indexes:
        #     print(R2_line)
        
        
    line_num += 1  # keep going through the files!
    
unknown_R1.close()
unknown_R2.close()
index_hopped_R1.close()
index_hopped_R2.close()

# close all of the perfectly matched index files
for file_pair in matched_output_files:
    for file in matched_output_files[file_pair]:
        file.close()

# open our markdown file and write all of the data we need to report to it
output = open("user_report.md", "w")
output.write(f"Number of reads that have each index pair:\n")
for index_pair in possible_pairs:
    output.write(f"{index_pair}: {possible_pairs[index_pair]}\n")

output.write(f"number of read-pairs with properly matched indexes: {perfect_matches}\n")

output.write(f"number of read pairs with index-hopping observed: {index_hopped}\n")

output.write(f"number of read pairs with unknown indexes: {unknown}\n")

total_reads = unknown + index_hopped + perfect_matches

percent_matched = (perfect_matches / total_reads) * 100

output.write(f"percentage of read-pairs with properly matched indexes: {percent_matched}%\n")

percent_hopped = (index_hopped / total_reads) * 100

output.write(f"percentage of read-pairs with index hopping observed: {percent_hopped}%\n")

percent_unknown = (unknown / total_reads) * 100

output.write(f"percentage of read-pairs with unknown indexes: {percent_unknown}%")

output.close() 

# for index_pair in possible_pairs:
#     if possible_pairs[index_pair] != 0:
#         print(index_pair, possible_pairs[index_pair])
#print(possible_pairs)

#print(matched_output_files)

# HAVE TO CLOSE INDEX MATCHED OUTPUT FILE AFTER YOU WRITE TO IT