#/usr/bin/env python

import bioinfo
import gzip
import argparse
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="A program to introduce yourself")
    parser.add_argument("-f", "--file", help="Name of the input fasta file", type=str, default="")
    parser.add_argument("-l", "--length", help="Length of the reads in the fastq file", type=int, default=0)
    parser.add_argument("-r", "--read_num", help="Read number of the input fastq file (ex. R1)", type=str, default="")
    #parser.add_argument("-o", "--output", help="Name of the output file", type=str, default="")
    return parser.parse_args()

args = get_args()

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    for i in range(args.length):
        lst.append(value)
    return lst

def populate_list(file: str) -> tuple[list, int]:
    """This function takes the name of a fastq file, creates an empty list, opens the fastq file, loops through every record, converts each quality score to its
    corresponding number, adds it to an ongoing sum for the quality scores at that position, and returns the list and a counter of the total number
    of lines in the file."""
    sum_list = []
    sum_list = init_list(sum_list)
    line_counter = 0
    with gzip.open(file, "rt") as fh:
        for i,line in enumerate(fh):
            line_counter = i
            if i % 4 == 3:
                line = line.strip()
                #print(len(line))
                for score_pos,score in enumerate(line):
                    #print(score_pos, end = " ")
                    #print(score, end = " ")
                    converted_score = bioinfo.convert_phred(score)
                    #print(converted_score, end = " ")
                    sum_list[score_pos] += converted_score
                #print(sum_list)
        
    return sum_list, line_counter + 1

# run populate_array function
my_list, num_lines = populate_list(args.file)
#print(my_list, num_lines)

# calculate the mean qscore at each base & print the resultant list
num_scores_at_base = num_lines / 4
#print(num_scores_at_base)
for i,sum_scores in enumerate(my_list):
     #print(sum_scores)
     #print(sum_scores / num_scores_at_base)
     my_list[i] = sum_scores / num_scores_at_base

print(f"# Base Pair\tMean Quality Score")
for i,mean_score in enumerate(my_list):
    print(i,"\t",mean_score)

base_pos = [x for x in range(args.length)]  # creates a list of 101 integers from 0 to 100
#print(base_pos)

fig,ax = plt.subplots()  # WHAT TYPE OF PLOT SHOULD I DO?
ax.bar(base_pos, my_list)
ax.set_title("Mean Quality Scores vs. Base Position")
ax.set_ylabel("Mean Quality Score")
ax.set_xlabel("Base Position")
plt.savefig(f"{args.read_num}_per_base_mean_qscore_dist.png")