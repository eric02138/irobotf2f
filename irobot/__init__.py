#!python
# -*- coding: utf-8 -*-
"""
iRobot Food2Fork Application Main Executable

"python main.py" runs the interactive version
TODO: cli version
"""
import os
import sys

class App:
    def __init__(self):
        f2f_api_key_path = os.path.join(os.path.abspath(os.sep), \
                                        'porchrock',
                                        'f2f_api_key.conf')
        self.f2f_api_key_path = f2f_api_key_path
        with open(self.f2f_api_key_path, "r") as f:
            self.f2f_api_key = f.read()

def main():
    app = App()
    print app.f2f_api_key_path
    print app.f2f_api_key

if __name__ == "__main__":
    main()

__date__ = "2019-02-01"
__version__ = "0.0.1"
__author__ = "Eric Mattison"
__maintainer__ = "Eric Mattison"
__email__ = "emattison@gmail.com"