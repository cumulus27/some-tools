#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
此处为文件的注释，详细的注释有助于代码的共同维护
此处描述这个文件实现的功能。

变量、类、方法命名风格，缩进方式等编码风格请参考Google开源项目Python编码风格规范，尽量保持代码风格的统一。
https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/

Usage:
此处描述这个包的使用方法。

写上作者和更新时间。
Author: Zhang san
Date: 2019.06.27
"""

# 导入写在最前面，先导入标准库再导入第三方库。
import os
import subprocess

from re import match
import numbers as num


# 类名用驼峰法命名
class PackageName:
    """
    Summary of class here.
    简要概括这个类是干啥的

    Longer class information....
    比较详细的介绍这个类实现的功能。

    介绍这个类初始化时需要的参数。介绍参数对使用者很重要。
    Attributes:
        path: An integer count of the eggs we have laid.
        likes_spam: A boolean indicating if we like SPAM or not.
    """

    def __init__(self, path, likes_spam=False):
        """Inits SampleClass with blah.
           在init方法中初始化对象的的属性，
           这个方法的参数就是创建对象的参数。
        """
        self.result_path = path
        self.likes_spam = likes_spam
        self.eggs = 0

    # 根据需求实现任意个方法，方法的命名用下划线连接
    def fetch_table_rows(self, big_table, keys, other_silly_variable=None):
        """
        介绍这个方法实现的功能。

        介绍参数以及返回值。
        :param big_table: 介绍参数
        :param keys:
        :param other_silly_variable:
        :return: 介绍返回值
        """

        # 打开写入文件等易出错的IO操作需要用try语句捕获可能出现的错误。
        # 文件操作建议用with语句块，避免忘记关闭文件引发错误。
        try:
            with open("/file/path", "w") as f:
                self.eggs = f.readlines()
        except IOError as e:
            print("Open file failed.")
            print(e)

    def show_the_parameter(self):
        """
        介绍这个方法实现的功能。

        介绍参数以及返回值。
        :param para_a: 在这里介绍参数
        :return: 在这里介绍返回值
        """

        # 变量的命名仍然以下划线连接
        first_parameter = 0
        self.likes_spam = 6

        return first_parameter + self.likes_spam

    def wait_to_complete(self):
        # TODO(Zhang San) 未完成的部分用todo注释说明，比较容易看见。
        pass

    @classmethod
    def check_number(cls, name, age=22):
        """
        不需要调用对象属性，但要调用其他类方法或者静态方法的方法可设置为
        类方法。

        :param name:
        :param age:
        :return:
        """
        i = 0

        # 在有技巧性的代码段前加注释以便于阅读
        # We use a weighted dictionary search to find out where i is in
        # the array.  We extrapolate position based on the largest num
        # in the array and the array size and then do binary search to
        # get the exact number.

        if i & (i - 1) == 0:  # True if i is 0 or a power of 2.
            cls.beautiful_print(i)

        return i

    @staticmethod
    def beautiful_print(value):
        """
        完全不需要调用对象属性的方法可以设置为静态方法，静态方
        法不需要传入self和class。

        :param value:
        :return:
        """
        print(value)


if __name__ == "__main__":

    # 这部分代码用于测试和调试，
    # 这部分内容不会被导入，尽量不要在这里实现功能
    path = "result/path/"

    test = PackageName(path)
    test.show_the_parameter()  # 尽量仅调用，用于调试测试。
