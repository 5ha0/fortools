import fortools.collction.decompress

def prefetch_open(path):
	file = open(path,'rb')
	if file.read(3) == 'MAM':
		file = decompress.decomp('path')
	return file
