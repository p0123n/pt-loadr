#! /usr/bin/env python3
#-*- coding: utf8 -*-

import os
import re
from glob import glob
from urllib.request import urlopen
from urllib.request import urlretrieve as wget

def getSiteFirst(rtpage='http://radio-t.com/'):
	page = str(urlopen(rtpage).read())
	preg = '(http(?:s)?://(?:[a-z\.\-/]+/)+([a-z_]+([0-9]{1,4}).mp3))'
	m = re.search(preg, page)
	try:
		return {'url': m.group(1), 'file': m.group(2), 'id': int(m.group(3))}
	except:
		print ("Something went wrong.")

def getFSLastID(siteFirst, where='.'):
	pattern = siteFirst['file'].replace(str(siteFirst['id']), '*')
	try:
		FSLast  = sorted(glob('%s/%s'%(where, pattern)), reverse=True)[0]
	except IndexError:
		return siteFirst['id'] - 3
	preg    = '(\d+).*\.mp3'
	m       = re.search(preg, FSLast)
	if (m.group is not None): return int(m.group(1))
	else: return siteFirst['id'] - 3

def rtSync(siteFirst, FSLastID, where='.'):
	__tmp1  = siteFirst['url'].replace(siteFirst['file'],     '[XXX]')
	__tmp2  = siteFirst['file'].replace(str(siteFirst['id']), '[XXX]')

	while (FSLastID < siteFirst['id']):
		FSLastID += 1
		pattern   = __tmp1.replace( '[XXX]', __tmp2.replace('[XXX]', str(FSLastID)) )
		# print ('Loading> ', pattern)
		wget(pattern, '%s/%s' % (where, __tmp2.replace('[XXX]', str(FSLastID)) ))
		keepLast(siteFirst)
	keepLast(siteFirst)

def keepLast(siteFirst, count=3, where='.'):
	pattern = siteFirst['file'].replace(str(siteFirst['id']), '*')
	__tmp3  = sorted(glob('%s/%s'%(where, pattern)), reverse=True)[count:]
	for ftd in __tmp3:
		print ('Removing: ', ftd)
		os.remove(ftd)

if __name__ == '__main__':
	siteFirst = getSiteFirst()
	FSLastID  = getFSLastID(siteFirst)
	rtSync(siteFirst, FSLastID)
