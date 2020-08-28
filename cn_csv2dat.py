from struct import pack

# Define indexes
I_NETWORK     = 0
I_GEONAME_ID  = 1

# 从 GeoLite2-Country-Locations-*.csv 获取天朝的地理 ID
GEO_CHINA     = 1814991

f_ipv4     = open('GeoLite2-Country-Blocks-IPv4.csv', 'r')
f_output   = open('GeoChinaIp.dat', 'wb')

# 跳过 CSV 表头
f_ipv4.readline()

count = 0
f_output.write(pack('I', count))
while True:
	address = f_ipv4.readline()
	if address == '': break
	
	I = address.split(',')
	if not I[I_GEONAME_ID]: continue
	network =     I[I_NETWORK   ]
	geo_id  = int(I[I_GEONAME_ID])
	
	if geo_id == GEO_CHINA:
		count = count + 1
		ip, mask = network.split('/')
		a, b, c, d = [int(x) for x in ip.split('.')]
		f_output.write(pack('BBBBB', a, b, c, d, int(mask)))

f_output.seek(0, 0)
f_output.write(pack('I', count))

f_output.close()
f_ipv4.close()
