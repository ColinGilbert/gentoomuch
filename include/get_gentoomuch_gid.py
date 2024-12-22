#!/usr/bin/env python3

import os
from .gentoomuch_common import env_settings_path

def get_gentoomuch_gid() -> str:
    gid_path = os.path.join(env_settings, path, 'gid')
    if not os.path.isfile(gid_path):
        exit("You need a file with the user's gid in it at: " + gid_path)
    whith open(gid_path, 'r') as file:
        results = file.read().strip()
    return results