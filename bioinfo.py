#!/usr/bin/env python

# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.2"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = None
RNA_bases = None

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33
    
def qual_score(phred_score: str) -> float:
    '''Computes the average phred score for the phred scores given'''
    sum_scores = 0
    for char in phred_score:
        sum_scores +=convert_phred(char)
    return sum_scores / len(phred_score)


def validate_base_seq(seq: str, RNAflag: bool=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    change  = "U" if RNAflag else "T"
    search = "ACGN" + change
    isSeq = seq.strip(search)
    return isSeq == "" 

def gc_content(seq: str) -> float:
    '''Returns GC content of a DNA sequence as a decimal between 0 and 1.'''
    seq = seq.upper()
    assert validate_base_seq(seq), "This is not a valid DNA sequence."
       
    G_count = seq.count("G")
    C_count = seq.count("C")
    return (G_count + C_count) / len(seq)

def reverse_complement(sequence: str) -> str:
    '''This function takes a string representing a sequence of DNA and returns a string representing 
    the reverse complement of that sequence'''
    assert validate_base_seq(sequence), "This is not a valid DNA sequence."
    rc = ""
    bps = {"A": "T", "T": "A", "C": "G", "G":"C", "N":"N"} 
    for i in range(len(sequence)-1, 0-1, -1):  # iterates through the string backwards
        rc += bps[sequence[i]]
    return rc

def calc_median(lst: list) -> float:
    '''Takes a list of numbers and calculates the median value of those numbers'''
    if len(lst) % 2 != 0:
        return lst[len(lst) // 2]
    else:
        return (lst[len(lst) // 2] + lst[(len(lst) // 2) -1])/2

def oneline_fasta(output_file: str, input_file: str):
    '''Takes the name of a fasta file and the name of an output file, opens the fasta file to read, parses through it, and condenses 
    the sequence lines to one line and writes to an output file with the given name'''
    with open(output_file, "w") as output:
        with open(input_file, "r") as fasta:
            first_line = True
            for line in fasta:
                if first_line:
                    output.write(line)
                    first_line = False
                elif line.startswith(">"):
                    output.write(f"\n{line}")
                else:
                    line = line.strip("\n")
                    output.write(line)
                
if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")