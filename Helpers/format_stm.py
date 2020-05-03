import sys
import re

useage_message='''
This script can trim the timestamp and file identifiers from all lines in the input file, e.g.AA 1 AA 726.72 729.4 <NA>
It also brings the two parts of a contracted word together
The output will have the same name as the input but with a .txt file extension

Useage:

    python trim-stm.py <in-file>

'''

def main():
    if len(sys.argv) < 2:
        print(useage_message)
        raise Exception("not enough arguments")

    stmfiles = sys.argv[1:]

    batch_format(stmfiles)

    print("The file(s) have been reformatted as txt files")


def format(stmfile):
    txtfile = stmfile.replace(".stm", ".txt")
    lines = []

    with open(stmfile, "r") as in_file:
        for line in in_file:
            line = re.sub(r"^[^>]*> ", "\n", line)
            line = line.replace(" '", "'")
            lines.append(line)

    with open(txtfile, "w") as out_file:
        out_file.writelines(lines)

def batch_format(stmfiles):
    for stmfile in stmfiles:
        format(stmfile)

if __name__ == "__main__":
    main()