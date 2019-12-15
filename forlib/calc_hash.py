import hashlib


def get_hash(path, type, blocksize=65536):
    file_name = path.split('\\')[-1:]
    file = open(path, 'rb')
    hasher_md5 = hashlib.md5()
    hasher_sha1 = hashlib.sha1()
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher_md5.update(buf)
        hasher_sha1.update(buf)
        buf = file.read(blocksize)
    file.close()
    hash_value = dict()
    hash_value["type"] = type
    hash_value["name"] = file_name
    hash_value["sha1"] = hasher_sha1.hexdigest()
    hash_value["md5"] = hasher_md5.hexdigest()
    return hash_value
