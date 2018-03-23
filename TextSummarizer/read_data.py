#!usr/bin/python

""" Module to read the data from 'PROJECT_HOME/data'.

	Data from all directories is retrieved and stored in
	'PROJECT_HOME/store/original_sents.pkl'
"""

import os
import config
import pickle
import numpy as np

PROJECT_HOME = config.PROJECT_HOME

""" Function to get the summary of a particular article.

	The content of the summary file and the line number 
	from where the event summary starts is given and all
	the sentences until the next dash marker ('-') are 
	retrieved.

	Parameters
	----------
	content: list of lists
		The content of the summary file.
	line: int
		Index of the line where the needed summary starts.

	Returns
	-------
	buf: list of lists
		The content of all the summary lines.	
"""

def get_input_data(content, line):
	# Initialize buffer
	buf = []

	# Retrieve each line until next '-'
	for i in range(line + 1, len(content)):
		if list(content[i])[0] == '-':
			return buf
		else:
			buf.append(content[i])
	        
	return buf

""" Function to retreive all records in a directory.

	Summary file of the directory is parsed for events
	and each event is stored along with the original 
	article in the InputDocs of the directory.

	Parameters
	----------
	folder: path
		Path to the given directory.
	name: str
		Name of the given directory.

	Returns
	-------
	folder_data: list of lists
		All records in the directory.
	skip_count: int
		Number of records skipped.
"""

def read_folder(folder, name):
	print ("Reading from ", name, "...")

	# Initialize folder_data and skip_count
	folder_data = []
	skip_count = 0

	# Read data in summary file
	print ("Checking all articles and corresponding data...")
	timelines = folder + "/timelines"
	for fname in os.listdir(timelines):
		with open(timelines + "/" + fname) as f:
			try:
				content = f.readlines()
			except Exception as e:
				# If no content in file
				print (e)
				continue
		# Remove whitespace
		content = [x.strip() for x in content]
		
	# List all files in InputDocs
	input_docs = folder + "/InputDocs/"
	inp = os.listdir(input_docs)

	# Check through content for all events
	for line in content:
		# If line starts with '2' then event is assumed
		if line[0] == '2':
			print ("Reading", line, "...")
			input_data = get_input_data(content, content.index(line))

			# Check if corresponding file exists in InputDocs
			try:
				if line in inp:
					ind = inp.index(line)
				docs = os.listdir(input_docs + inp[ind])
				for doc in docs:
					with open(input_docs + inp[ind] + "/" + doc) as f:
						lines = f.readlines()
					lines = [x.strip() for x in lines]
					folder_data.append([lines, input_data])
			except Exception as e:
				# If file not found
				skip_count += 1
				print ("Data not found, skipping...")
				continue

	return folder_data, skip_count

""" Function to check for and retrieve all data in the
	directories in Timeline17

	All data is stored in 'PROJECT_HOME/store/original_sents.pkl'

	Parameters
	----------
	None

	Returns
	-------
	None
"""
def read_data():
	# Path to data home, initialize data
	PATH = PROJECT_HOME + 'data/Timeline17/Data/'
	data = []

	# For each directory in data home, retrieve data
	print ("Listing all article groups...")
	skip_counts = []
	folders = os.listdir(PATH)
	for folder in folders:
		folder_data, skip_count = read_folder(PATH + "/" + folder, folder)
		data.append(folder_data)
		skip_counts.append(skip_count)
	print ("Done.")

	# Flatten data
	data = [item for sublist in data for item in sublist]

	# Put together all data from all the directories
	print ("Compiling all data together...")
	final_data = []
	for i in range(len(data)):
		# All original docs
		sens = []
		for x in data[i][0]:
			x = x.split(' ')
			sens.append(x)

		# All summaries
		summ = []
		for y in data[i][1]:
			y = y.split(' ')
			summ.append(y)

		# Create corresponding instances
		instance = [sens, summ]
		final_data.append(instance)
	print ("Done.")

	# Summarize data situation
	print ("")
	print ("Data found ->")
	print ("Total rows = ", len(final_data))
	print ("Total skipped = ", sum(skip_counts))
	print ("")

	# Store data
	print ("Storing data...")
	data_out = open(PROJECT_HOME + 'store/original_sents.pkl', 'wb')
	pickle.dump(final_data, data_out)
	data_out.close()
	print ("Done.")

def main():
	read_data()

if __name__ == "__main__":
	main()