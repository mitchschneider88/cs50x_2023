import csv
import sys


def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py STRCOUNTS_filename DNA_filename")

    strcounts = []

    with open(sys.argv[1], "r") as strcounts_file:
        reader = csv.DictReader(strcounts_file)
        for row in reader:
            strcounts.append(row)
            row["AGATC"] = int(row["AGATC"])
            row["AATG"] = int(row["AATG"])
            row["TATC"] = int(row["TATC"])
            try:
                row["TTTTTTCT"] = int(row["TTTTTTCT"])
                row["TCTAG"] = int(row["TCTAG"])
                row["GATA"] = int(row["GATA"])
                row["GAAA"] = int(row["GAAA"])
                row["TCTG"] = int(row["TCTG"])
            except:
                continue

    with open(sys.argv[2], "r") as dna_file:
        sequence = dna_file.read()

    if len(strcounts) > 3:
        subsequence = ["AGATC", "AATG", "TATC", "TTTTTTCT", "TCTAG", "GATA", "GAAA", "TCTG"]
        subsequence_results = {"AGATC": 0, "AATG": 0, "TATC": 0, "TTTTTTCT": 0, "TCTAG": 0, "GATA": 0, "GAAA": 0, "TCTG": 0}
    else:
        subsequence = ["AGATC", "AATG", "TATC"]
        subsequence_results = {"AGATC": 0, "AATG": 0, "TATC": 0}

    for i in range(len(subsequence)):
        subsequence_results[subsequence[i]] = longest_match(sequence, subsequence[i])

    matches = 0

    for i in range(len(strcounts)):
        result = all(subsequence_results.get(key) == strcounts[i].get(key) for key in subsequence_results)
        if result == True:
            name = strcounts[i].get('name')
            matches += 1

    if matches == 1:
        print(name)
    else:
        print("No match")


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