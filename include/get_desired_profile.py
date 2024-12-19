#!/usr/bin/env python3

import os
from .gentoomuch_common import desired_profile_path


def get_desired_profile():
    if os.path.isfile(desired_profile_path):
        with open(desired_profile_path) as file:
            results = file.read().strip()
            return results
    else:
        exit("You need to set a profile")