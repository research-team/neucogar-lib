import os
from collections import defaultdict

"""
After simulation merge splitted files by threads and save
"""

# Get path of txt resutls


results_path = input("Enter path to the result folder")
# Create structure - the dict of a lists. Main file (string) : child files (list)
files_map = defaultdict(list)
# Build tree of rough (threaded) files
files_list = [file for file in os.listdir(results_path) if os.path.isfile("{}/{}".format(results_path, file))]

for threaded_file in files_list:
	main_file_name = "{}.{}".format(threaded_file.split('-')[0],    # Get body name of the file without thread number
	                                threaded_file.split('.')[-1])   # Get file format
	# Add child file to the main_file's list in dictionary
	files_map[main_file_name].append(threaded_file)
# For every main_file in dict an his childs list
for main_file, child_files in files_map.items():
	# Write to the main file
	with open("{}/{}".format(results_path, main_file), 'w') as f_main:
		# Get data from every child files and write to the main file
		for threaded_file in child_files:
			with open("{}/{}".format(results_path, threaded_file), 'r') as f_child:
				for line in f_child:
					f_main.write(line)
			# Delete finished needless child file
			os.remove("{}/{}".format(results_path, threaded_file))