import subprocess
import sys
import re
import format_stm
import datetime
# prepare data
# done in a common directory for all aligners
srt_time_format = "%H:%M:%S,%f"

def time_to_seconds(time):
    return time.hour * 3600 + time.minute * 60 + time.second + time.microsecond * 0.000001

def prepare_data(data_path):
    ls = subprocess.run(["ls", data_path], encoding='utf-8', stdout=subprocess.PIPE).stdout
    stm_files = ["{}/{}".format(data_path, file) for file in ls.split("\n") if ".stm" in file]
    format_stm.batch_format(stm_files)

def write_stm_data(stm_files_path):
    ls = subprocess.run(["ls", stm_files_path], encoding='utf-8', stdout=subprocess.PIPE).stdout
    stm_files = ["{}/{}".format(stm_files_path, file) for file in ls.split("\n") if ".stm" in file]
    for file in stm_files:
        data = []
        with open(file, "r") as in_file:
            for line in in_file:
                times = re.findall(r"\s[0-9]+[\.0-9]*\s[0-9]+[\.0-9]*\s", line)[0].strip().split(" ")
                caption = re.sub(r"^[^>]*> ", "\n", line).replace(" '", "'")
                data.append({"start": times[0], "end": times[1], "duration": float(times[1]) - float(times[0]), "captionlength": len(caption.split(" "))})
        
        out = file.replace(".stm", "-stm-data.csv")
        with open(out, "w") as out_file:
            out_file.write("start,end,duration,captionlength\n")
            for entry in data:
                out_file.write("{},{},{},{}\n".format(entry["start"], entry["end"], entry["duration"], entry["captionlength"]))

def write_srt_data(srt_files_path):
    ls = subprocess.run(["ls", srt_files_path], encoding='utf-8', stdout=subprocess.PIPE).stdout
    srt_files = ["{}/{}".format(srt_files_path, file) for file in ls.split("\n") if ".srt" in file]
    for file in srt_files:
        data = []
        with open(file, "r") as in_file:
            is_caption_line = False
            for line in in_file:
                if "-->" in line:
                    times = [time_to_seconds(datetime.datetime.strptime(time.strip(), srt_time_format)) for time in line.split("-->")]
                    data.append({"start": times[0], "end": times[1], "duration": times[1] - times[0]})
                    is_caption_line = True
                elif is_caption_line:
                    data[len(data) - 1]["captionlength"] = len(line.split(" "))
                    is_caption_line = False

        out = file.replace(".srt", "-srt-data.csv")
        with open(out, "w") as out_file:
            out_file.write("start,end,duration,captionlength\n")
            for entry in data:
                out_file.write("{},{},{},{}\n".format(entry["start"], entry["end"], entry["duration"], entry["captionlength"]))