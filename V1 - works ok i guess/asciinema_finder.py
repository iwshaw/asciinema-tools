#!/usr/bin/env python
import os, shutil, fnmatch

def find_files():
    file_names = [ "*@10.10.*.json" ] 
    for root, dirnames, filenames in os.walk("."):
            for target in file_names:
                for candidate_filename in fnmatch.filter(filenames, target):
                    print("GRABBING ",candidate_filename)
                    shutil.copy(os.path.join(root, candidate_filename), ".")
