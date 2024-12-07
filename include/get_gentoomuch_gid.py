#!/usr/bin/env python3

import os


def get_gid() -> str:
    eturn open(os.path.join(env_settings_path, 'gid'), 'r').read().strip()
