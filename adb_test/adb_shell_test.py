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
    def __init__(self, command_file, device_id=None, shell=False):
        self.device_id = device_id

        self.first_command = None
        self.second_command = None
        self.shell = shell

        self.command_iter = self.get_one_test_command(command_file)

    def prepare_the_command(self):
        full_command = self.second_command
        print(full_command)

        self.process_command(full_command)
        input("Press Enter to continue...\n")

    @classmethod
    def write_in_file(cls, file_path, value):
        try:
            with open(file_path, "a+") as f:
                f.write(value)
        except IOError as e:
            print("Write failed.")
            print(e)

    @classmethod
    def get_one_test_command(cls, path):
        with open(path, "r") as f:
            while True:
                name = f.readline().strip()
                if not name:
                    raise StopIteration
                yield name

    def process_command(self, full_command):
        try:
            p = subprocess.Popen(self.first_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate(full_command.encode("utf-8"))
            p.kill()
            print(stdout.decode("utf-8"))
            print(stderr.decode("utf-8"))
        except IOError as e:
            print("Write failed.")
            print(e)

    def start_find(self, command):
        self.first_command = command
        print(self.first_command)

        while True:
            try:
                line = next(self.command_iter)
            except StopIteration:
                print("Execute all the test command, finished.")
                break
            else:
                line = line.strip()
                if "adb shell " in line:
                    self.second_command = line.replace("adb shell ", "")
                else:
                    self.second_command = line

                self.prepare_the_command()

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

    command_path = "data/command.txt"
    # devices_id = "324291421094"

    start_time = time.time()
    find = PermissionFind(command_path)
    find.start_test()
    cost_time = time.time() - start_time

    print(f"\nTest complete, cost {cost_time:.2f}s.")

