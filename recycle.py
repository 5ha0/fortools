import forrtools.collection.file_open


def recycle_open(path):
	file_kind = path.split('\\')[-1]
	if file_kind.find('R') != -1:
		file_extension = path.split('.')[1]
		file = file_open.extension_file_open(file_extension,path)
		return file
	elif file_kind.find('I') != -1:
		file = open(path,'rb')
		return file
