#!/usr/bin/env python3

import os
from .gentoomuch_common import arch_config_path, output_path, desired_stage_path, desired_profile_path
from .swap_stage import swap_stage
from .create_composefile import create_composefile
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_desired_profile import get_desired_profile
from .get_desired_stage import get_desired_stage
from .get_gentoomuch_uid import get_gentoomuch_uid


def freshroot(arch: str, profile: str):
    desired_profile = open(desired_profile_path).read().strip()
    print("    Trying to start fresh root with profile " + desired_profile + " and stage definition gentoomuch/builder")
    #create_composefile(output_path)
    swap_stage(arch, desired_profile, "gentoomuch/builder", False) 
    code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash")
    if code == 0:
        pass
