#!/usr/bin/env python
import glob, os
import asciinema_reader as ar
import asciinema_finder as af

af.find_files()

os.mkdir("./processed")
os.chdir(".")
for file in glob.glob("*.json"):
    print(file, "PROCESSING ...")
    ar.process_file(file)
    print(file, "... DONE")
    os.remove(file)
