#!/usr/bin/env python3

import os
from .gentoomuch_common import desired_profile_path


def get_desired_profile():
    return ((True, open(desired_profile_path, 'r').read().strip()) if os.path.isfile(desired_profile_path) else (False, ''))