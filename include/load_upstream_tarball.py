#!/usr/bin/env python3

import os, shutil
from pathlib import Path
from .gentoomuch_common import gentoo_upstream_url, gentoo_signing_key, stages_path, asc_ext
from .verify_tarball import verify_tarball
from .containerize import containerize

def load_upstream_tarball(arch, profile, path):
    fname = os.path.split(path)[1]
    new_tarball_path = os.path.join(stages_path, fname)
    code = os.system("cp " + path + " " + new_tarball_path)
    if code == 0:
        pass
    code = os.system("cp " + path + ".asc " + new_tarball_path)
    if code == 0:
        pass
    print("Containerizing upstream tarball")
    return containerize(path, arch, profile, stage_define = '', upstream = True)
