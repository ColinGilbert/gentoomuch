#!/usr/bin/env python3

from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_dockerized_profile_name import get_dockerized_profile_name


def get_local_stage4_name(arch: str, profile: str, stagedef: str, kernel_defines: str):
    return 'stage4-' + arch + '-' + get_dockerized_profile_name(profile) + '-' + get_dockerized_stagedef_name(stagedef) + '-' + kernel_defines + '.tar.gz'
