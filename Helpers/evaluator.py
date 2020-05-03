import sys
sys.path.insert(1, '../')
import subprocess
import re
import os
import time

import format_stm
import prepare_data
import CurrentForcedAlignementTools.aeneas.aeneas_interface
import CurrentForcedAlignementTools.gentle.gentle_interface

useage_message = '''
python3 evaluator.py -d <path> -a <aligner>

[options for measuring speed of the aligner]
-d <path>                path for where the tedlium data is stored
-a <aligner>                 select aligner to use ("aeneas", or "gentle")
--repetitions <num>
--prepare-texts     this can be used to prepare the stm files as texts ready for alignment

[These parse some data from the alignment files as csv]
--write-stm-data
--write-srt-data <aligner>

[these options should be used to perform analysis on the data and the generated srts compared to the originals]
-compare
--help
'''

# should be relative path
data_path = ""
test_repetitions = 3
aligner = ""
do_alignment = False
prepare_texts = False
write_data_from_stm = False
write_data_from_srt = False

import datetime
def main():
    # t = "0:00:22,200000"
    # format = "%H:%M:%S,%f"
    # x = datetime.datetime.strptime(t, format).time()
    # print(x)

    # exit()

    parse_inputs(sys.argv[1:])

    if os.path.isdir(data_path):
        if prepare_texts:
            prepare_data.prepare_data(data_path)
        if do_alignment and data_path is not "":
            get_alignment_times(data_path, aligner)
        if write_data_from_stm:
            prepare_data.write_stm_data(data_path)
        if write_data_from_srt:
            if aligner is "aeneas" or aligner is "gentle":
                message = "A valid aligner must be entered: {}".format(aligner)
                raise Exception(message)
            prepare_data.write_srt_data("{}/{}".format(data_path, aligner))


def parse_inputs(args):
    global data_path
    global test_repetitions
    global do_alignment
    global aligner
    global prepare_texts
    global write_data_from_stm
    global write_data_from_srt

    if len(args) == 0:
        print(useage_message)
        exit()
    while len(args) != 0:
        arg = args.pop(0)
        if arg == "-d":
            data_path = os.path.abspath(args.pop(0))
        elif arg == "-a":
            do_alignment = True
            aligner = args.pop(0)
        elif arg == "--repetitions":
            test_repetitions = int(args.pop(0))
        elif arg == "--prepare-texts":
            prepare_texts = True
        elif arg == "--write-stm-data":
            write_data_from_stm = True
        elif arg == "--write-srt-data":
            write_data_from_srt = True
            aligner = args.pop(0)
        else:
            print(useage_message)
            exit()

def get_alignment_times(data_path, aligner_option):
    aligner = 0
    if "aeneas" in aligner_option:
        aligner = CurrentForcedAlignementTools.aeneas.aeneas_interface.Aligner(data_path)
    elif "gentle" in aligner_option:
        aligner = CurrentForcedAlignementTools.gentle.gentle_interface.Aligner(data_path)
    else:
        Exception("A Valid aligner must be entered: {}".format(aligner))
    
    # might need to prepare data into txt first
    aligner.start_container()
    ls = subprocess.run(["ls", data_path], encoding='utf-8', stdout=subprocess.PIPE).stdout
    files = [file.strip(".txt") for file in ls.split("\n") if ".txt" in file]
    data = []
    for file in files:
        for i in range(test_repetitions):
            start_time = time.time()
            aligner.align(file)
            end_time = time.time()
            # file size/ audio length may be good to store too
            data.append({"file": file, "attempt": i + 1, "duration": end_time - start_time})
    
    with open("{}/timings.csv".format(aligner.alignment_out_path), "w") as out_file:
        out_file.write("file,attempt,duration\n")
        for entry in data:
            out_file.write("{},{},{}\n".format(entry["file"], entry["attempt"], entry["duration"]))

    aligner.stop_container()

# measure time taken to align [measuring is done but nothing has been calculated from the data]
    # measure multiple things and compute mean and variance to 
        # align multiple times to account for sampling errors
        # [important note, different samples are for approximating normal dist, samples of the same thing account for measuring errors]
    # store all measurment somewhere
    # store mean and variance for each file (normalised to ) [doesnt actually make sense]
    # store mean and variance across all files
# process
    # get an instance of an aligner
    # start container
    # do alignment per file multiple times
        # measure alignment time per alignment operation
        # results will be stored
    # stop container

# measure difference between aligners srt times and tedlium reference times
    # try to calculate the distribution of differences
        # do difference per line
            # store extra info per line, e.g. num of characters, start diff, end diff, duration diff
        # this will give a good idea on how different the alignments are
# process
    # compare the srt caption times to those in the reference
        # need to know where each is
            # for each caption in each compute difference in start, end and duration
                # store those and the num of chars in the caption into another file
    # with this data other things can be computed which will be seperate funcitons
        # e.g dists of start end and duration, correlation of length and accuracy
    # accuracy will be a scoring that takes into account all three time measurements
        # I dont know if duration is needed


if __name__ == "__main__":
    main()