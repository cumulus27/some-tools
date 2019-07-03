#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Find the file with given permission.
"""

import os
import re
import time
import subprocess


class PermissionFind:
    def __init__(self, path_r, device_id=None, path="/", shell=False, skip_proc=True):
        self.path_r = path_r
        self.device_id = device_id

        self.first_command = None
        self.second_command = None
        self.path = path
        self.shell = shell
        self.skip_proc = skip_proc

        self.error_log_path = os.path.join(self.path_r, "error_log.txt")

    def find_global_read(self):
        full_command = " ".join([self.second_command, "-type f -perm /o=r -exec ls -l '{}' \;"])
        print(full_command)

        file_path = os.path.join(self.path_r, f"global_read_{self.device_id}.txt")
        self.process_command(file_path, full_command)

    def find_global_write(self):

        full_command = " ".join([self.second_command, "-type f -perm /o=w -exec ls -l '{}' \;"])
        print(full_command)

        file_path = os.path.join(self.path_r, f"global_write_{self.device_id}.txt")
        self.process_command(file_path, full_command)

    def find_777(self):
        full_command = " ".join([self.second_command, "-type f -perm 777 -exec ls -l '{}' \;"])
        print(full_command)

        file_path = os.path.join(self.path_r, f"global_777_{self.device_id}.txt")
        self.process_command(file_path, full_command)

    def find_suid(self, file_path):
        us_re = re.compile("[r-][w-][sStT][r-][w-].[r-][w-].")
        path_result = os.path.join(self.path_r, f"suid_{self.device_id}.txt")

        try:
            with open(file_path, "r") as f:
                for line in f.readlines():
                    match = re.match(us_re, line, flags=0)
                    if match:
                        self.write_in_file(path_result, line)
        except IOError as e:
            print("Open file failed.")
            print(e)

    def find_guid(self, file_path):
        us_re = re.compile("[r-][w-].[r-][w-][sStT][r-][w-].")
        path_result = os.path.join(self.path_r, f"guid_{self.device_id}.txt")

        try:
            with open(file_path, "r") as f:
                for line in f.readlines():
                    match = re.match(us_re, line, flags=0)
                    if match:
                        self.write_in_file(path_result, line)
        except IOError as e:
            print("Open file failed.")
            print(e)

    @classmethod
    def write_in_file(cls, file_path, value):
        try:
            with open(file_path, "a+") as f:
                f.write(value)
        except IOError as e:
            print("Write failed.")
            print(e)

    def process_command(self, output_path, full_command):
        try:
            with open(output_path, "wb") as f:
                p = subprocess.Popen(self.first_command, stdin=subprocess.PIPE, stdout=f,
                                     stderr=subprocess.PIPE, shell=True)
                stdout, stderr = p.communicate(full_command.encode("utf-8"))
                p.kill()
                # print(stderr.decode("utf-8"))
                self.write_in_file(self.error_log_path, "\n\n" + output_path + "\n")
                self.write_in_file(self.error_log_path, stderr.decode("utf-8"))
        except IOError as e:
            print("Write failed.")
            print(e)

    def start_find(self, command):
        self.first_command = command
        print(self.first_command)
        self.second_command = f"find {self.path}"
        if self.skip_proc:
            self.second_command = " ".join([self.second_command, "-path /proc -prune -o"])

        self.find_global_read()
        self.find_global_write()
        self.find_777()

        full_command = " ".join(["ls", "-l", "-R"])
        print(full_command)
        file_path = os.path.join(self.path_r, f"all_files_{self.device_id}.txt")

        if not os.path.exists(file_path):
            self.process_command(file_path, full_command)

        self.find_suid(file_path)
        self.find_guid(file_path)

    def start_test(self):
        devices_info = subprocess.run(["adb", "devices"], capture_output=True)
        stdout = devices_info.stdout.decode("utf-8")
        stderr = devices_info.stderr.decode("utf-8")
        if devices_info.returncode != 0:
            print("Failed to start adb server, please check.")
            print(stderr)
            raise RuntimeError
        elif "\n" not in stdout.strip():
            print(stdout)
            print("There is no connected devices, please check.")
            raise RuntimeError

        print(stdout)

        ready_re = "device\n"
        no_per_re = "no permissions"
        ready_device = re.findall(ready_re, stdout)
        no_per_device = re.findall(no_per_re, stdout)

        device_id_re = "\n.*\tdevice"
        ready_device_ids = [one_id.split("\t")[0].strip() for one_id in re.findall(device_id_re, stdout)]

        if self.shell:
            print("Works on linux shell.")
            self.start_find("")
            return

        if len(ready_device) == 0:
            print("There is no ready devices to connect.")
            raise RuntimeError
        elif len(ready_device) >= 2 and not self.device_id:
            print("You don't set device id, and there is more than one device connected.")
            raise RuntimeError
        elif len(ready_device) == 1 and not self.device_id:
            self.device_id = ready_device_ids[0]
            self.start_find("adb shell")
        elif self.device_id in ready_device_ids:
            self.start_find(f"adb -s {self.device_id} shell")
        else:
            print("There is no devices same as your set.")
            print(f"{self.device_id} vs {ready_device_ids}")
            raise RuntimeError


if __name__ == "__main__":

    result_path = "data/result/"
    # devices_id = "324291421094"

    try:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
    except Exception as e:
        print("Error in create path: {}".format(e))

    start_time = time.time()
    find = PermissionFind(result_path)
    find.start_test()
    cost_time = time.time() - start_time

    print(f"\nTest complete, cost {cost_time:.2f}s.")

