#!/usr/bin/env python
from datetime import datetime
import string

current_line = []

def handle_first_line(first_line):
	timestamp_index = first_line.find("timestamp")
	start_time_index = timestamp_index + 12
	start_time_unix = first_line[start_time_index:(start_time_index+10)]
	global start_time_unix_int	# lol python is crazy
	start_time_unix_int = int(start_time_unix)
	start_time = datetime.fromtimestamp(start_time_unix_int).isoformat()
	return "Recording begins: "+start_time+"\n"

def convert_time(offset):
	offset_float = float(offset)	# the string is a float...
	offset_int = int(offset_float)	# ...now the float is an int lol python you joker
	this_utc = datetime.fromtimestamp(start_time_unix_int + offset_int).isoformat()[11:]
	return this_utc

def print_to_file(filename, entry):
    filename = "./processed/"+filename+".txt"
    with open(filename, 'a') as f:
        print(entry, file=f)

def process_file(filename):
    global current_line
    with open(filename, errors='ignore') as f:
        print_to_file(filename, handle_first_line(f.readline())) # get the initial metadata

        while True: # this looks like a terrible idea but welcome to python
            new_line = f.readline()
            if not new_line:
                print_to_file(filename, "EOF Reached")
                break
            else:
                line_elements = new_line.split(',')
                this_time = line_elements[0][1:]
                content = line_elements[2]
                if(len(content)>9): # if it's more than one character, get the time and return the time and the line
                    print_to_file(filename, convert_time(this_time)+"    "+content[:-2])
                elif(len(content)==9 and content.find("\"\\r\\n\"]")): # if the user hit enter, write the line
                    print_to_file(filename, "\nUSER ENTRY:\n" + convert_time(this_time)+"     "+''.join(current_line) + "\n")
                    current_line = []
                else: # if it's one character, append it to the current line
                    current_line.append(content[2:-3])
