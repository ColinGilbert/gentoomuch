#!/usr/bin/env python3

import os
from .gentoomuch_common import env_settings_path

def get_gentoomuch_jobs() -> str:
    jobs = open(os.path.join(env_settings_path, 'jobs'), 'r').read().strip()
    if not jobs.isnumeric():
        exit("ERROR: jobs needs to be a number!")
    return jobs