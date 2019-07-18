#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Get apk file from drozer, then export the apk file.
"""

import os
import re
import time
import subprocess


class DrozerTest(object):

    def __init__(self, command):
        self.command = command
        self.apk_list = None

    def get_apk_list(self):
        # TODO(py) resolve the problem that drozer can't work in python3.
        output = subprocess.run(["adb forward tcp:31415 tcp:31415"], shell=True, capture_output=True)
        print(output)
        print("\n")

        p = subprocess.Popen("export PATH=\"/usr/bin/python2:$PATH\";drozer console connect", stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        stdout, stderr = p.communicate()
        # stdout, stderr = p.communicate(self.command.encode("utf-8"))
        print(stderr.decode("utf-8"))

        self.apk_list = stdout.decode("utf-8")

    def read_apk_list(self):
        try:
            with open("list.txt", "r") as f:
                lines = f.readlines()
        except IOError:
            print("Error in read file.")
            raise RuntimeError
        else:
            self.apk_list = [package.strip().split(": ")[1] for package in lines]

    def pull_apk_file(self):
        print("\n")
        for package in self.apk_list:
            p = subprocess.Popen("adb shell", stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate(f"pm path {package}".encode("utf-8"))

            stdout = stdout.decode("utf-8")
            if ":" in stdout:
                path = stdout.strip().split(":")[1]
                print(f"Get the path :{path}")

                subprocess.run(f"adb pull {path} data/{package}.apk", shell=True)
            else:
                print(f"Can't find package {package}.")


if __name__ == "__main__":

    drozer_command = "run test.permission.info"
    test = DrozerTest(drozer_command)
    test.read_apk_list()

    for line in test.apk_list:
        print(line)

    test.pull_apk_file()
