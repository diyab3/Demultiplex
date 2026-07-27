import bioinfo

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    for i in range(101):
        lst.append(value)
    return lst

file = ""

def populate_list(file: str) -> tuple[list, int]:
    """This function takes the name of a fastq file, creates an empty list, opens the fastq file, loops through every record, converts each quality score to its
    corresponding number, adds it to an ongoing sum for the quality scores at that position, and returns the list and a counter of the total number
    of lines in the file."""
    sum_list = []
    sum_list = init_list(sum_list)
    with open(file, "r") as fh:
        for i,line in enumerate(fh):
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
    return sum_list, i + 1