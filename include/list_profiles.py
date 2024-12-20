#!/usr/bin/env python3

import os, docker
from include.gentoomuch_common import arch_config_path, desired_profile_path, profiles_path, output_path
from .docker_stage_exists import docker_stage_exists
from .get_desired_profile import get_desired_profile
from .get_profiles import get_profiles

def list_profiles(arch):
    desired = get_desired_profile()
    print("Listing compatible system profiles:")
    for p in get_profiles():
        if docker_stage_exists(arch, p, 'gentoomuch/builder', False):
            bootstrapped_indicator = 'GOOD TO GO :)  '
        elif docker_stage_exists(arch, p, '', True):
            bootstrapped_indicator = 'UPSTREAM READY '
        else:
            bootstrapped_indicator = 'NOT INSTALLED  '
        if p == desired:
            desired_indicator = '[*]'
        else:
            desired_indicator = '[ ]'
        print(' ' + bootstrapped_indicator + ' ' + desired_indicator + '       ' + p)
    exit()
