#!/usr/bin/python

# rogueclown
# March 2013
#
# subdfinder_rcmaker.py
#
# takes a list of domains in a text file, and creates an rc file for recon-ng that
# uses both dns brute force and web searching techniques to enumerate subdomains
# of the listed domains.  
#
# also, resolves IPs for each of the subdomains, and tries to pull common interesting
# files that are publicly available on the subdomains.
#
# licensed under the WTFPL: http://www.wtfpl.net/txt/copying/
#
#######################################################################
#                                                                     #
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE              #
#                    Version 2, December 2004                         #
#                                                                     #
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>                    #
#                                                                     #
# Everyone is permitted to copy and distribute verbatim or modified   #
# copies of this license document, and changing it is allowed as long #
# as the name is changed.                                             #                                                                     #                                                                     #
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE              #
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION   #
#                                                                     #
#  0. You just DO WHAT THE FUCK YOU WANT TO.                          #
#######################################################################

from optparse import OptionParser
from sys import exit

# handle command line options
parser = OptionParser(usage="usage: %prog -d domain_filename -o output_filename [-w workspace]")

parser.add_option("-d", "--domainfile", dest="domainfile", type="string")
parser.add_option("-w", "--workspace", dest="workspace", type="string")
parser.add_option("-o", "--outfile", dest="outfile", type="string")

(opts, args) = parser.parse_args()

mandatories = ["domainfile", "outfile"]
for m in mandatories:
	if not opts.__dict__[m]:
		print "mandatory option is missing.\n"
		parser.print_help()
		exit(-1)

# function for writing script lines to output file
# including new line at end of each script directive
def scriptwrite(text):
	outputfile.write(text + "\n")

# parse list of domains from domain file
try:
	f = open(opts.domainfile, 'r')
	domainlist = f.readlines()
	domainlist = [domain.rstrip() for domain in domainlist]
	f.close()
except:
	print "error reading " + opts.domainlist
	exit(-1)

# prepare output file for writing
try:
	outputfile = open(opts.outfile, 'w')
except:
	print "error opening " + opts.outfile + " for writing."
	exit(-1)

# set workspace, if that was provided
# otherwise, recon-ng defaults to using "default" workspace
if opts.workspace:
	scriptwrite("set workspace " + opts.workspace)

# enumerate subdomains of all domains in domainlist

for domain in domainlist:
	scriptwrite("use recon/hosts/gather/dns/brute_force")
	scriptwrite("set domain " + domain)
	scriptwrite("run")
	scriptwrite("exit")
	for resource in ["baidu", "bing", "google", "ip_neighbor", "netcraft", "shodan", "yahoo"]:
		scriptwrite("use recon/hosts/gather/http/" + resource)
		scriptwrite("set domain " + domain)
		scriptwrite("run")
		scriptwrite("exit")

# perform discovery on all found domains and subdomains, once
# database is built out
scriptwrite("use recon/hosts/enum/dns/resolve")
scriptwrite("run")
scriptwrite("exit")
scriptwrite("use discovery/info_disclosure/http/interesting_files")
scriptwrite("run")
scriptwrite("exit")
scriptwrite("hosts")

# close output file
outputfile.close()
