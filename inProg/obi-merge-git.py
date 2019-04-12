#! /usr/bin/env python
"""Script to manage concurrent RPD development using Git in a Gitflow methodology.
"""

import os
import re
import sys
import platform
import errno
from glob import glob
from shutil import copyfile
from argparse import ArgumentParser
import configparser
from subprocess import Popen, PIPE, STDOUT, call

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
CURRENT_DIR = os.getcwd()


try:
	os.chdir(SCRIPT_DIR)  # Change to script directory

	# ArgumentParser to parse arguments and options
	arg_parser = ArgumentParser(description="OBI GIT Merge Script")
	arg_parser.add_argument('action', choices=['startDevelop', 'finishDevelop', 'refreshDevelop', 'startRelease',
											   'finishRelease', 'startHotfix', 'finishHotfix', 'bugfix'], help='Gitflow action.')
	arg_parser.add_argument('name', help='Name of a feature, release or hotfix depending on the action chosen.')
	arg_parser.add_argument('-p', '--push', action="store_true", default=False, help='Push directly to origin.')
	arg_parser.add_argument('-a', '--autoOpen', action="store_true", default=False,
						help='Automatically opens new RPD after merge.')
	arg_parser.add_argument('-t', '--tag', action="store", help='Specify tag annotation if finishing a release.')
	arg_parser.add_argument('-c', '--config', default='config.ini', help='Config file to be used. Default: "config.ini"')
	args = arg_parser.parse_args()

	# Parse config parameters
	config_file = args.config
	if not os.path.exists(config_file):
		print('\n**Config file %s not found. Exiting.'.format(config_file))
		sys.exit(1)

	conf_parser = configparser.ConfigParser()
	conf_parser.read(config_file)

	OBIEE_VERSION = conf_parser.get('OBIEE', 'OBIEE_VERSION')
	CLIENT_ONLY = conf_parser.getboolean('OBIEE', 'CLIENT_ONLY')
	OBIEE_HOME = os.path.abspath(conf_parser.get('OBIEE', 'OBIEE_HOME'))

	# Optional path setting for clients and server and mixed installations
	OBIEE_CLIENT = os.path.abspath(conf_parser.get('OBIEE', 'OBIEE_CLIENT'))
	if CLIENT_ONLY is False and OBIEE_CLIENT == '':
		OBIEE_CLIENT = os.path.join(OBIEE_HOME, 'user_projects', 'domains')
	elif CLIENT_ONLY is True and OBIEE_CLIENT == '':
		OBIEE_CLIENT = OBIEE_HOME
	else:
		OBIEE_CLIENT = os.path.abspath(conf_parser.get('OBIEE', 'OBIEE_CLIENT'))

	RPD_PW = conf_parser.get('OBIEE', 'RPD_PW')



	GIT_EXE = conf_parser.get('Git', 'GIT_EXE')
	GIT_REPO = conf_parser.get('Git', 'GIT_REPO')
	GIT_RPD = conf_parser.get('Git', 'GIT_RPD')
	GIT_REMOTE = conf_parser.get('Git', 'GIT_REMOTE')
	GIT_DEVELOP = conf_parser.get('Git', 'GIT_DEVELOP')
	GIT_MASTER = conf_parser.get('Git', 'GIT_MASTER')
	FEATURE_PREFIX = conf_parser.get('Git', 'FEATURE_PREFIX')
	HOTFIX_PREFIX = conf_parser.get('Git', 'HOTFIX_PREFIX')
	RELEASE_PREFIX = conf_parser.get('Git', 'RELEASE_PREFIX')

	ACTION = args.action
	NAME = args.name
	PUSH = args.push
	TAG = args.tag
	AUTO_OPEN = args.autoOpen

	if (ACTION == 'startDevelop' or ACTION == 'finishDevelop' or ACTION == 'refreshDevelop') and NAME is None:
		arg_parser.print_help()
		print('\n\tError: Name (-n, --name) must be specified.')
	
except Exception as e:
	print('\n\nException caught:'+(e))
	print('\n\n\tFailed to get command line arguments. Exiting.')
	sys.exit(1)

class GITTOOL:
	def test(self):
		print("test")
		
	def start_develop(self,feature):
		feature_name = FEATURE_PREFIX + feature
		print(feature_name)
		print(GIT_DEVELOP)
	#branch(feature_name, GIT_DEVELOP)
	
	def finish_feature(feature):
		feature_name = FEATURE_PREFIX + feature
		response = git_bi_merge(GIT_DEVELOP, feature_name)
		if response:
			merge_success(GIT_DEVELOP, feature_name, True)

		
def start_develop(feature):
	feature_name = FEATURE_PREFIX + feature
	print(feature_name)
	print(GIT_DEVELOP)
	branch(feature_name, GIT_DEVELOP)

def finish_feature(feature):
	feature_name = FEATURE_PREFIX + feature
	print(feature_name)
	response = git_bi_merge(GIT_DEVELOP, feature_name)
	#if response:
		#merge_success(GIT_DEVELOP, feature_name, True)


def branch(branch_name, base):
	#Creates a new branch from an existing branch (base)
	checkout(base)
	pull()
	out = cmd(['checkout', '-b', branch_name, base])
	print(str(out))
	return out

def checkout(branch_name):
	#Checks out a Git branch.

	print("Checking out....."+branch_name+" branch")
	cmd(['checkout', branch_name])
	
def pull():
	"""Pulls latest changes from the tracked remote Git repository."""
	cmd(['fetch'])
	out = cmd(['pull'])
	print("Pull Request"+ str(out))
	return out
	
def cmd(command):
	"""
	Executes a Git command and reports an error if one is detected.
	E.g.	cmd(['pull'])
	"""

	command = [GIT_EXE, '-C', GIT_REPO] + command
	print(command)
	output = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
	if output[1]:
		print(output[1])
	return output


def git_bi_merge(trunk, branch_name):
	"""Merges an RPD branch into a different trunk branch, calling the Admin Tool to resolve OBI conflicts."""
	print("GIT BI MERGE"+trunk+branch_name)
	merge_out = merge(trunk, branch_name)

def merge(trunk, branch_name, no_ff=False):
	"""Merges a Git branch to a trunk."""
	print("\nMERGE"+trunk+branch_name)
	checkout(trunk)
	out = pull()
	if out[1]:
		if re.search('no tracking information', out[1]):  # Check if pull failed because there is no remote
			if trunk in [GIT_DEVELOP, GIT_MASTER]:  # If trunk is not one of the main trunks we should exit with failure
				return out

	print('Merging %s into %s...' % (branch_name, trunk))
	if no_ff:
		out = cmd(['merge', '--no-ff', branch_name])
		print(str(out))
	else:
		out = cmd(['merge', branch_name])
		print(str(out))
	return out
	

def main():
	#git=GITTOOL()
	

	if ACTION == 'startDevelop':
		start_develop(NAME) #git.start_develop(NAME) #
	elif ACTION == 'finishDevelop':
		finish_feature(NAME)
		print('finishFeature Feature')
	elif ACTION == 'refreshDevelop':
		print('refreshFeature Feature')#refresh_feature(NAME)
	elif ACTION == 'startRelease':
		print('Test')

if __name__ == "__main__":
	print('main')
	main()
