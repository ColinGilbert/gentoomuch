#!/usr/bin/env python3

import os
from .gentoomuch_common import env_settings_path

def get_gentoomuch_gid() -> str:
    return open(os.path.join(env_settings_path, 'gid'), 'r').read().strip()
