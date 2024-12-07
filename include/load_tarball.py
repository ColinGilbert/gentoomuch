#!/usr/bin/env python3

import os, shutil
from pathlib import Path
from .gentoomuch_common import gentoo_upstream_url, gentoo_signing_key, stages_path, asc_ext
from .verify_tarball import verify_tarball
from .containerize import containerize

def load_tarball(arch, profile, path):
    fname = os.path.split(path)[1]
    if verify_tarball(path):
        new_tarball_path = os.path.join(stages_path, fname)
        #print(new_tarball_path)
        code = os.system("cp " + path + " " + new_tarball_path)
        if code == 0:
            pass
        # Dockerize that thing, ya'll
        print("INFO: Containerizing upstream tarball")
        return containerize(path, arch, profile, '', bool(True))
