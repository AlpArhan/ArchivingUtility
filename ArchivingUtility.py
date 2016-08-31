### archiving Utility for files 90 days old ###
##--------------------------------------------------------------------------------------------------------##
### This is a recursive function that can zip an entire folder from the source directory you have stated to an archive directory you wish ###
### Program is designed to archive files only if their last modified date is greater than 90 days. ###
#!/usr/bin/python

import sys
import zipfile
import os
import os, glob
import os.path
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import datetime
import time
import shutil
import argparse
import sys, getopt
from optparse import OptionParser
import errno

## Creates a zipfile for the files inside the folder ###
class ZipUtilities:
    def toZip(self, file, filename):
		print "Creating zip, src: %s, dest: %s" % (file, filename)
		zip_file = zipfile.ZipFile(filename, 'w')

		# |file| must point to a directory
		try:
			self.addFolderToZip(zip_file, file)
		finally:
			zip_file.close()

		# If the archive is empty then don't keep it around
		if not zip_file.infolist():
			os.remove(filename)


    def addFolderToZip(self, zip_file, folder):
		cut_off_time_days = 0
		today = date.today()

        # If the directory is empty, then there is no work to do.
		contents = os.listdir(folder)
		if not contents:
			print "Folder is empty, no work to do"
			return

		for file in contents:
			full_path = os.path.join(folder, file)
			print "Processing path %s" % full_path

			# If this is a folder, then go inside
			if os.path.isdir(full_path):
				print 'Entering folder'
				self.addFolderToZip(zip_file, full_path)
				continue

			# Ignore if this is not a file (e.g. a symlink)
			if not os.path.isfile(full_path):
				print "Path is not a file. Ignoring"
				continue

			last_modified_date = datetime.date.fromtimestamp(os.path.getmtime(full_path))
			print "Last modified: %s" % str(last_modified_date)
			duration = today - last_modified_date
			if cut_off_time_days <= duration.days:
				print "File/folder is older than %d days" % cut_off_time_days
				print "File: %s Duration: %s" % (full_path, duration)
				zip_file.write(full_path)

				print ('Removing the file: ') + str(full_path)
				os.remove(full_path)
				print ('File %s is removed') % (str(full_path))



# Check if the output path is under or same path with the source path
def is_child_path(parent, child):
	parent_components = os.path.abspath(parent).split(os.sep)
	child_components = os.path.abspath(child).split(os.sep)
	if not parent_components:
		return False

	return parent_components == child_components[:len(parent_components)]


def main():

	parser = argparse.ArgumentParser(prog='Archive Utility',epilog='',description = 'Description: Archive Utility for zipping files that are more than 90 days old.')
	parser.add_argument("Archive_name" , metavar='<Archive_Name>', help="Archive Name for '.zip' file")
	parser.add_argument("src_dir" , metavar='<src_dir>', help="Source Directory: The directory that is going to be archived.")
	parser.add_argument("output_dir" , metavar='<output_dir>' , help="Output Directory: The directory where the zip files will be stored.")
	args = parser.parse_args()
	root_directory = args.src_dir
	archive_directory = args.output_dir
	name_suffix = args.Archive_name

	## Checks whether the given src_dir and output_dir exists.
	if not os.path.isdir(root_directory): ## To check if the root_directory exists ##
		print "Source directory is not a valid folder %s" % root_directory
		return 1

	if not os.path.isdir(archive_directory): ## To check if the archive_directory exists ##
		print "Output directory is not a valid folder %s" % archive_directory
		return 1

	## Checks if src_dir and output_dir are on the same path.
	if is_child_path(root_directory,archive_directory):
		print "Error[3]: Source and Output directories cannot be under the same path. Change the paths."
		print "Archive Utility is closed."
		return 1

	utilities = ZipUtilities()
	timestr = time.strftime("_%Y%m%d")
	filename = '%s%s.zip' % (name_suffix , timestr)
	output_path = os.path.join(archive_directory, filename)
	## Checks if there is a zip file that already exists with the same name.
	if os.path.exists(output_path):
		print "%s already exists.Try again with a different archive name." % output_path
		quit()
	else:
		print "%s is created." %  output_path

	## Checks if any other error can occur due to source and output directories that is not mentioned.
	try:
		utilities.toZip(root_directory, output_path)
	except Exception as e:
		print "An error ocurred[4]: There is a problem with source directory and/or output directory."
		print e
		return 1

	return 0


if __name__ == '__main__':
	status = main()
	sys.exit(status)
