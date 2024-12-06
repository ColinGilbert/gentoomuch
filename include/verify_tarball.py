#!/usr/bin/env python3

import os, gnupg, hashlib
from .gentoomuch_common import stages_path, gpg_path, asc_ext, digests_ext, gentoo_signing_key, gentoo_upstream_url
from .read_file_lines import read_file_lines


def verify_tarball(filepath : str):
    gpg = gnupg.GPG()
    #public_keys = gpg.list_keys() 
    #print(public_keys)
    #filename = os.path.relpath(filepath, stages_path)
    print("INFO: Verifying signature of file " +  filepath)
    digests_filepath = filepath + digests_ext
    digests_file = open(digests_filepath, 'rb').read()
    #print(digests_file)
    #print(gpg.verify(digests_file))
    if not gpg.verify(digests_file):
        print("ERROR: Failed to verify signature file: " + filepath + digests_ext)
        return False
    found = False
    digests_file = open(filepath + digests_ext, 'rb').read()
    lines = digests_file.decode('ascii').split('\n')
    ctr = 0
    # We are going to find the line in the .asc file that corresponds to our SHA512 sig and obtain it.
    while not found:
        if ctr + 1 == len(lines):
            exit("ERROR: Reached end of " + filename + digests_ext + " without finding the tarball's SHA512 hash.")
            # return False
        if lines[ctr]  == '# SHA512 HASH':
            desired_sha512 = lines[ctr + 1].split(' ')[0]
            found = True
        ctr += 1
    print("INFO: Seeking hash:   " + desired_sha512)
    sha512 = hashlib.sha512()
    BLOCK_SIZE = 65536
    with open(filepath, 'rb') as f:
        buf = f.read(BLOCK_SIZE)
        while len(buf) > 0:
            sha512.update(buf)
            buf = f.read(BLOCK_SIZE)
    print("INFO: Hashed value is " + sha512.hexdigest())
    if desired_sha512 != sha512.hexdigest():
        exit("ERROR: Wrong SHA512 for " + filename)
    return True
