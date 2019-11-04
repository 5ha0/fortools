import hashlib


def get_md5_hash(path, blocksize=65536):
    file = open(path, 'rb')
    hasher = hashlib.md5()
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
    file.close()
    hash_value = hasher.hexdigest()
    print('MD5: '+str(hash_value))
    return hash_value


def get_sha1_hash(path, blocksize=65536):
    file = open(path, 'rb')
    hasher = hashlib.sha1()
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
    file.close()
    hash_value = hasher.hexdigest()
    print('SHA1: ' + str(hash_value))
    return hash_value
