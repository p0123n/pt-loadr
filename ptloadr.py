#! /usr/bin/env python3
#-*- coding: utf8 -*-

from os.path import expanduser
HOME = expanduser("~")

import sys
sys.path.append("plugins") 

import default   as df

def main(args):

	#
	# Radio-t
	#
	if len(args) == 0 or 'radiot' in args:
		# download opts
		www = 'http://radio-t.com/'
		reg = '(http(?:s)?://(?:[0-9a-z\.\-/]+/)+([a-z_]+([0-9]{1,4}).mp3))'

		# local path opts
		dst  = HOME + '/Music/radiot'

		site_first_file = df.getSiteFirst(www, reg)
		df.sync(
			site_first_file,
			df.getFSLastID(site_first_file, dst),
			dst
		)
	#
	# JSPirates
	#
	if len(args) == 0 or 'jspirates' in args:
		# download opts
		www = 'http://jspirates.com/jsp_audio.xml'
		reg = '<guid>(http(?:s)?://(?:[0-9a-z\.\-/]+/)+([a-z_]+([0-9]{1,4}).mp3))</guid>'

		# local path opts
		dst  = HOME + '/Music/jspirates'

		site_first_file = df.getSiteFirst(www, reg)
		df.sync(
			site_first_file,
			df.getFSLastID(site_first_file, dst),
			dst
		)

if __name__ == '__main__':
	main(sys.argv[1:])

