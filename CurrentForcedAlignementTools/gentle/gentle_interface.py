import subprocess
import sys
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, script_dir)
import json_to_srt

dockerfile = "lowerquality/gentle"
image_name = "gentle"

class Aligner():
    data_path = ""
    alignment_out_path = ""

    def __init__(self, data_path):
        self.data_path = data_path
        self.alignment_out_path = "{}/gentle".format(data_path)
        if not os.path.isdir(self.alignment_out_path):
            os.mkdir(self.alignment_out_path)

    def start_container(self):
        container_list = subprocess.run(["docker", "container", "ls", "-a"], encoding='utf-8', stdout=subprocess.PIPE).stdout
        if image_name in container_list:
            subprocess.run(["docker", "container", "start", image_name])
        else:
            # subprocess.run(["docker", "container", "run", "-dtv", "{}:/workdir".format(self.data_path), "-p", "8080:8765", "--name", image_name, dockerfile])
            subprocess.run(["docker", "container", "run", "-dtv", "{}:/workdir".format(self.data_path), "--name", image_name, dockerfile])

    def stop_container(self):
        subprocess.run(["docker", "container", "stop", image_name])

    def align(self, file_name):
        subprocess.run(["docker", "container", "exec", image_name, "python", "/gentle/align.py", "--nthreads", "1", "-o", "/workdir/gentle/{}.json".format(file_name), "/workdir/{}.sph".format(file_name), "/workdir/{}.txt".format(file_name)])
        out_name = "{}/{}.json".format(self.alignment_out_path, file_name)
        json_to_srt.json_to_srt(out_name)
