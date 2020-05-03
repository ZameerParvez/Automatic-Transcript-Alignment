import subprocess
import sys
import os


aligner_dir = os.path.dirname(os.path.realpath(__file__))
dockerfile = "{}/.".format(aligner_dir)
image_name = "aeneas"

class Aligner():
    config_string = "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"
    data_path = ""
    alignment_out_path = ""

    def __init__(self, data_path):
        self.data_path = data_path
        self.alignment_out_path = "{}/aeneas".format(data_path)
        if not os.path.isdir(self.alignment_out_path):
            os.mkdir(self.alignment_out_path)

    def start_container(self):
        image_list = subprocess.run(["docker", "image", "ls", "-a"], encoding='utf-8', stdout=subprocess.PIPE).stdout
        if image_name not in image_list:
            subprocess.run(["docker", "image", "build", "-t", image_name, dockerfile])
        
        container_list = subprocess.run(["docker", "container", "ls", "-a"], encoding='utf-8', stdout=subprocess.PIPE).stdout
        if image_name in container_list:
            subprocess.run(["docker", "container", "start", image_name])
        else:
            subprocess.run(["docker", "container", "run", "-dtv", "{}:/workdir".format(self.data_path), "--name", image_name, image_name])

    def stop_container(self):
        subprocess.run(["docker", "container", "stop", image_name])

    # these will be the names of the files in the volume directory
    def align(self, file_name):
        subprocess.run(["docker", "container", "exec", image_name, "python", "-m", "aeneas.tools.execute_task", "{}.sph".format(file_name), "{}.txt".format(file_name), self.config_string, "aeneas/{}.srt".format(file_name)])
