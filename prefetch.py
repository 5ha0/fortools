import fortools.collction.decompress

def open(path):
	file = open(path,'rb')
		if file.read(3) == 'MAM':
			f.close()
			decompress = decompress.decomp('path')
			return decompress
	return file
