#!/usr/bin/env python3

import re
from .gentoomuch_common import image_tag_base
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name


def get_docker_tag(arch, profile, stage_define, upstream : bool):
    cleaned_profile = get_dockerized_profile_name(profile) 
    cleaned_stage_define = get_dockerized_stagedef_name(stage_define) 
    tag_tail = ''
    if upstream == True:
        tag_tail = arch + '-' + cleaned_profile + ':upstream' # We use the upstream stage3.
    else:
        tag_tail = arch + '-' + cleaned_profile + '-' + cleaned_stage_define + ':latest' # We use the locally-built stage3.
    #print(image_tag_base + tag_tail)
    return image_tag_base + tag_tail
