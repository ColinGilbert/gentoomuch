#!/usr/bin/env python3

import os, docker
from .gentoomuch_common import desired_profile_path
from .docker_stage_exists import docker_stage_exists
from .get_profiles import get_profiles

def set_desired_profile(arch, profile):
    if profile not in get_profiles() or not (docker_stage_exists(arch, profile, 'gentoomuch-builder', False) or docker_stage_exists(arch, profile, '', True)):
        exit("Profile not bootstrapped yet.")
    print("Setting Gentoomuch profile to " + profile)
    if os.path.isfile(desired_profile_path):
        os.remove(desired_profile_path)
    open(desired_profile_path, 'w').write(profile)
