# this assumes that a newline in the source text file delimits captions, so that they are timestamped seperatley
# inputs are just the json file returned by gentle

import datetime
import json
import sys
useage_message = '''To use this script you need to supply the json file that is output by gentle aligner, it will then output an srt file, where each caption is delimited by the newlines in the original transcript.

[Example useage]
python json-to-srt.py syncmap.json
'''

def main():
    if len(sys.argv) < 2:
        print(useage_message)
        raise Exception("not enough arguments")

    alignmentfiles = sys.argv[1:]
    batch_format(alignmentfiles)
    print("Formatting of json as srt is done")

def to_srt_time(seconds):
    micro_seconds = int((seconds % 1) * 1000000)
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return "{}:{}:{},{}".format(hours, minutes, seconds, micro_seconds)

def json_to_srt(json_file):
    outputfile = json_file.replace(".json", ".srt")

    with open(json_file, "r") as in_file:
        alignment_dict = json.load(in_file)
        captions = [caption.replace("\n", "").strip() for caption in alignment_dict["transcript"].split("\n\n")]
        transcript = alignment_dict["transcript"]
        aligned_words = [word for word in alignment_dict["words"] if word["case"] == "success"]
        caption_alignments = []

        caption_alignments.append({"start": to_srt_time(aligned_words[0]["start"])})
        for i in range(len(aligned_words) - 1):
            if "\n\n" in transcript[aligned_words[i]["endOffset"]: aligned_words[i+1]["startOffset"] + 1]:
                caption_alignments[len(caption_alignments) - 1]["end"] = to_srt_time(aligned_words[i]["end"])
                caption_alignments.append({"start": to_srt_time(aligned_words[i + 1]["start"])})
        caption_alignments[len(caption_alignments) - 1]["end"] = to_srt_time(aligned_words[len(aligned_words) - 1]["end"])

        with open(outputfile, "w") as out_file:
            line_template = "{num}\n{start} --> {end}\n{caption}\n\n"
            for i in range(len(captions)):
                out_file.write(line_template.format(num = i + 1, start = caption_alignments[i]["start"], end = caption_alignments[i]["end"], caption = captions[i]))

def batch_format(json_files):
    for file in json_files:
        json_to_srt(file)

if __name__ == "__main__":
    main()