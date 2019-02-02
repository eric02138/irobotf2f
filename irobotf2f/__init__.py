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
        f2f_api_key_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        f2f_api_key_path = os.path.join(f2f_api_key_dir, 'apikey.conf')
        print f2f_api_key_path
        try:
            with open(f2f_api_key_path, "r") as f:
                self.f2f_api_key = f.read()
        except Exception:
            print "Could not read api key at {0}".format(f2f_api_key_path)
            raise

def main():
    app = App()

if __name__ == "__main__":
    main()

__date__ = "2019-02-01"
__version__ = "0.0.1"
__author__ = "Eric Mattison"
__maintainer__ = "Eric Mattison"
__email__ = "emattison@gmail.com"