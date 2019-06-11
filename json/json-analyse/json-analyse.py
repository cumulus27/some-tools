#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Analyse the json.
"""

import json
import copy
from collections import abc


class JsonAnalyse(object):

    def __init__(self):
        self.str = None
        self.json = None
        self.value_list = None
        self.value_list_value = None
        self.changed_json = None
        self.changed_request = None

    def load_json(self, path):
        try:
            with open(path, "r") as f:
                self.str = f.readline()
        except IOError as e:
            print(f"IOError in file read: {e}")
            raise RuntimeError
        else:
            try:
                self.json = json.loads(self.str)
            except TypeError as e:
                print(f"TypeError in json load: {e}")
                raise RuntimeError

    def load_json_file(self, path):
        try:
            with open(path, "r") as f:
                self.json = json.load(f)
        except IOError as e:
            print(f"IOError in file read: {e}")
            raise RuntimeError
        except TypeError as e:
            print(f"TypeError in json load: {e}")
            raise RuntimeError

    def show_beautiful(self):
        print(json.dumps(self.json, sort_keys=True, indent=4))

    def start_analyse(self):
        self.value_list = {-1: []}
        self.value_list_value = {}
        self.get_next_branch(self.json, [])
        del self.value_list[-1]

    def get_next_branch(self, parent, path):
        if isinstance(parent, abc.Mapping):
            for key, value in parent.items():
                new_path = copy.deepcopy(path)
                new_path.append(key)
                # print(new_path)
                self.get_next_branch(value, new_path)
        elif isinstance(parent, abc.MutableSequence):
            for index, item in enumerate(parent):
                new_path = copy.deepcopy(path)
                new_path.append(index)
                # print(new_path)
                self.get_next_branch(item, new_path)
        else:
            find_keys = self.value_list.keys()
            max_key = max(find_keys)
            self.value_list.update({max_key+1: path})
            self.value_list_value.update({max_key+1: parent})

    def show_value_list(self):
        print(json.dumps(self.value_list, sort_keys=True, indent=4))

    def input_count(self):
        """获取总数"""
        return len(self.value_list)

    def get_input_name(self, i):
        """获取name"""
        return "-".join([str(index) for index in self.value_list[i]])

    def item(self, i):
        """获取value"""
        return self.value_list_value[i]

    def set_input_value(self, i, value):
        """改变第i个参数的值为value"""
        self.changed_json = copy.deepcopy(self.json)
        change_path = "self.changed_json"

        item = ""
        for item in self.value_list[i]:
            if isinstance(item, str):
                change_path = change_path + "[\"" + item + "\"]"
            else:
                change_path = change_path + "[" + str(item) + "]"
        else:
            change_path = change_path + "=value"

        exec(change_path)
        self.changed_request = json.dumps(self.changed_json, separators=(',', ':'))

        print(json.dumps(self.changed_json, sort_keys=True, indent=4))

        print(self.changed_request)


if __name__ == "__main__":

    file_path = "osconfeed.json"

    analysis = JsonAnalyse()
    # analysis.load_json(file_path)
    analysis.load_json_file(file_path)
    # analysis.show_beautiful()

    analysis.start_analyse()
    analysis.show_value_list()

    print(analysis.input_count())

    print(analysis.get_input_name(10))

    print(analysis.item(10))

    print(type(analysis.json))

    # analysis.set_input_value(55, "Hello world.")