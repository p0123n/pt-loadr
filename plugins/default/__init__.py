import os
import re
from glob import glob
from urllib.request import urlopen
from urllib.request import urlretrieve as wget

def getSiteFirst(rtpage, preg):
	page = str(urlopen(rtpage).read())
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
	preg    = '(\d+)\.mp3'
	m       = re.search(preg, FSLast)
	if (m.group is not None): return int(m.group(1))
	else: return siteFirst['id'] - 3

def sync(siteFirst, FSLastID, where='.'):
	__tmp1  = siteFirst['url'].replace(siteFirst['file'],     '[XXX]')
	__tmp2  = siteFirst['file'].replace(str(siteFirst['id']), '[XXX]')

	while (FSLastID < siteFirst['id']):
		FSLastID += 1
		pattern   = __tmp1.replace( '[XXX]', __tmp2.replace('[XXX]', str(FSLastID)) )
		# print ('Loading> ', pattern)
		try:
			wget(pattern, '%s/%s' % (where, __tmp2.replace('[XXX]', str(FSLastID)) ))
		except:
			print ('Loading was failed > ', pattern)
		else:
			keepLast(siteFirst, where=where)
	keepLast(siteFirst, where=where)

def keepLast(siteFirst, count=3, where='.'):
	pattern = siteFirst['file'].replace(str(siteFirst['id']), '*')
	__tmp3  = sorted(glob('%s/%s'%(where, pattern)), reverse=True)[count:]
	for ftd in __tmp3:
		print ('Removing: ', ftd)
		os.remove(ftd)
