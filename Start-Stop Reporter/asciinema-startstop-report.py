import os, shutil, fnmatch
from datetime import datetime

global local_time_offset
local_time_offset = 10800 # UAE time - three hours ahead (in seconds)
global filename
filename = os.path.basename(os.getcwd()) + " Start-Stop Times Report.txt"
global current_team_number
current_team_number = "000"
global current_team_member
current_team_member = "not-a-member"

def handle_first_line(first_line):
	timestamp_index = first_line.find("timestamp")
	start_time_index = timestamp_index + 12
	start_time_unix = first_line[start_time_index:(start_time_index+10)]
	global start_time_unix_int	# lol python is crazy
	start_time_unix_int = int(start_time_unix)
	start_time = datetime.fromtimestamp(start_time_unix_int + 10800).isoformat()
	return start_time_unix_int

def convert_time(start_time, offset):
    global local_time_offset
    offset_float = float(offset)    # the string is a float...
    offset_int = int(offset_float)  # ...now the float is an int lol python you joker
    this_local_time = datetime.fromtimestamp(start_time + offset_int + local_time_offset).isoformat()[11:] # 10800s is three hours for local time
    return this_local_time

def format_to_nicetime(time):
    global local_time_offset
    time_code_hour = time[:2]
    time_code_hour = str(local_time_offset + int(time_code_hour))
    time_code_mins = time[2:4]
    time_code_secs = time[4:6]
    return time_code_hour+":"+time_code_mins+":"+time_code_secs

def print_to_file(entry):
    with open(filename, 'a') as f:
        print(entry, file=f)

def process_file(filename):
    global current_team_number
    global current_team_member
    global start_time_unix_int
    team_number_index_start = filename.find("@10.10") + 7
    team_number_index_end = filename.find(".", team_number_index_start+1)
    team_number = filename[team_number_index_start:team_number_index_end]
    team_number = str(team_number).zfill(3)
    if (team_number != current_team_number):
        print_to_file("\nTeam "+team_number)
        current_team_number = team_number
        current_team_member = "not-a-member" # force restatement of the player

    if(filename.find("alpha") != -1):
        team_member = "alpha"
    elif(filename.find("beta")!= -1):
        team_member = "beta"
    elif(filename.find("gamma") != -1):
        team_member = "gamma"
    if (team_member != current_team_member):
        print_to_file("----Player "+team_member)
        current_team_member = team_member

    with open(filename, errors='ignore') as f:
        start_time_unix_int = handle_first_line(f.readline())
        start_time = convert_time(start_time_unix_int, 0)
        file_time_message = "--------"+start_time+" -> "
        while True: # this looks like a terrible idea but welcome to python
            new_line = f.readline()
            if not new_line:
                end_time = convert_time(start_time_unix_int, this_time)
                file_time_message += end_time
                print_to_file(file_time_message)
                break
            else:
                line_elements = new_line.split(',')
                this_time = line_elements[0][1:]

opening_message = os.path.basename(os.getcwd()) + " Start and Stop Times\nALL TIMES ARE LOCAL UAE TIME (+3 HOURS FROM THE SOURCE FILES)\n"
print_to_file(opening_message)

file_names = [ "*@10.10.*.json" ] 
for root, dirnames, filenames in os.walk("."):
    for target in file_names:
        for file in fnmatch.filter(filenames, target):
            process_file(os.path.join(root, file))
