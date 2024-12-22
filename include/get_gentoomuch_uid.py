#!/usr/bin/env python3

import os
from .gentoomuch_common import env_settings_path

def get_gentoomuch_uid() -> str:
    uid_path = os.path.join(env_settings, path, 'uid')
    if not os.path.isfile(uid_path):
        exit("You need a file with the user's uid in it at: " + uid_path)
    whith open(uid_path, 'r') as file:
        results = file.read().strip()
    return results