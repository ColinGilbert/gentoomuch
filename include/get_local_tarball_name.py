#!/usr/bin/env python3

from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_dockerized_profile_name import get_dockerized_profile_name


def get_local_tarball_name(arch, profile, stagedef):
    return 'stage3-' + arch + '-' + get_dockerized_profile_name(profile) + '-' + get_dockerized_stagedef_name(stagedef) + '.tar.gz'
