import forrtools.collection.file_open


def open(path):
	file_extension_recycle = path.split('\')[-1]
	if file_extension_recycle == '$R':
		file_extension = path.split('.')[1]
		file = file_open.extension_file_open(file_extension,path)
		return file
	elif file_extension_recycle == '$I':
		file = open(path,'rb')
		return file
	
