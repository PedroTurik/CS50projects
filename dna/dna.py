import csv
import sys


def main():

    #Check for command-line usage
    database = sys.argv[1]
    dna = sys.argv[2]
    if len(sys.argv) != 3:
        print("usage: python dna.py data.csv sequence.txt")
        quit()

    #Read database file into a variable
    with open(database, "r") as datafile:
        reader = csv.DictReader(datafile)
        dict_list = list(reader)
    with open(dna, "r") as txtfile:
        sequence = txtfile.read()

    STRs = []
    for x in range(1, len(reader.fieldnames)):
        STRs = STRs + [reader.fieldnames[x]]

    mc = []
    for y in range(len(STRs)):
        mc = mc + [longest_match(sequence, STRs[y])]

    for i in range(len(dict_list)):
        matches = 0
        for j in range(1, len(reader.fieldnames)):
            if int(dict_list[i][reader.fieldnames[j]]) == mc[j - 1]:
                matches += 1
        if matches == len(reader.fieldnames) - 1:
            print(dict_list[i]["name"])
            quit()

    print("No match")
# TODO: Read DNA sequence file into a variable
# TODO: Find longest match of each STR in DNA sequence
# TODO: Check database for matching profiles

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()