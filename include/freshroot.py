#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path
from .swap_stage import swap_stage


def freshroot(arch: str, profile: str):
    print("    Trying to start fresh root with profile " + profile + " and stage definition gentoomuch-builder")
    #create_composefile(output_path)
    swap_stage(arch, profile, "gentoomuch-builder", False) 
    code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash")
    if code == 0:
        pass
