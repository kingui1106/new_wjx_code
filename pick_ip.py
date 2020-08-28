from __future__ import print_function
from struct import unpack
from random import randint
try:
	# Python 2
	from httplib import HTTPConnection
	from urllib import urlencode
except:
	# Python 3
	from urllib.parse import urlencode
	from http.client import HTTPConnection

# Run following in http://music.163.com/ to get payload; where 64634 is any id that does not work outside China.
# with(asrsea("{\"ids\":\"[64634]\",\"br\":128000,\"csrf_token\":\"\"}","010001","00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7","0CoJUm6Qyw8W8jud")) JSON.stringify({ params: encText, encSecKey });
payload = {"params":"1jGcS1W77hIKvP/5xvJN4DRJP4qWjWdVXio+Iy4ztTwUQpfehnmLdxKkz8y7tUO1kkQXqe0Cv3wCRrgTfqjoa+ripG5hqvZ1+YUYODcz7es=","encSecKey":"21bfcacc1ee1459e04b0a9970ea7b6775524af3309168549f82084266721a2f29dba89f9be2c84ca627f8369eb64f61aa2002e6bea90a29651445154e96cb0052e12077d6c5094dfcc72f22c07879abc6a5eb69e50ab6fb4293140036b65a465fcd6ca5a54d0672c8a1ec393bc9f22771d4a17762a8d8792e32c522e826ff46f"}
payload = urlencode(payload)

def check_ip(ip):
	"""Connect to netease and check if the ip is availiable.
	
	Args:
		ip (str): IP Address to be checked
		
	Returns:
		bool: True if valid, False otherwise.
	"""
	conn = HTTPConnection('music.163.com', 80)
	headers = {
		"Accept":"*/*",
		"Content-Type":"application/x-www-form-urlencoded",
		"Content-Length":len(payload),
		"Referer":"http//music.163.com/",
		"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
		"X-Real-IP": ip
	}
	conn.request('POST', '/weapi/song/enhance/player/url?csrf_token=', payload, headers)
	resp = conn.getresponse()
	r = str(resp.read())
	conn.close()
	return '"url":"http' in r

def pick_ip():
	f_input = open('GeoChinaIp.dat', 'rb')
	count ,= unpack('I', f_input.read(4))
	while True:
		f_input.seek(4 + randint(0, count - 1) * 5, 0)
		ip, mask = unpack('>IB', f_input.read(5))

		size = pow(2, 32 - mask)

		a = (ip >> 24) & 255
		b = (ip >> 16) & 255
		c = (ip >>  8) & 255
		d = (ip >>  0) & 255

		print('%d.%d.%d.%d/%d; size = 0x%x' % (a, b, c, d, mask, size))

		ip += randint(0, size - 1)

		a = (ip >> 24) & 255
		b = (ip >> 16) & 255
		c = (ip >>  8) & 255
		d = (ip >>  0) & 255

		str_ip = '%d.%d.%d.%d' % (a, b, c, d)
		print('IP: %s, verifying...' % str_ip, end='')

		if check_ip(str_ip):
			print(' OK!')
			break
		print(' Failed!')
	f_input.close()
	return str_ip


