#!/usr/bin/env python3

import os, gnupg, hashlib
from .gentoomuch_common import stages_path, gpg_path, asc_ext, digests_ext, gentoo_signing_key, gentoo_upstream_url
from .read_file_lines import read_file_lines


def verify_tarball(path : str):
    gpg = gnupg.GPG()
    print("INFO: Verifying signature of file " +  path)
    asc_path = path + asc_ext
    if not os.path.isfile(path):
        print("VERIFY TARBALL: Could not find " + path)
        return False
    if not os.path.isfile(asc_path):
        print("VERIFY TARBALL: Could not find " + asc_path)
        return False
    if not gpg.verify_file(open(asc_path, 'rb'), path):
        print("VERIFY TARBALL: Failed to verify file " + path)
        return False
    return True
