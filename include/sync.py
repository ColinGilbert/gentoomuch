#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path
from .create_composefile import create_composefile

def sync():
    print("GENTOOMUCH: Syncing Portage...")
    code = os.system("cd " + output_path + " && docker-compose run gentoomuch-updater /bin/bash -c 'emerge -v --sync'")
    return code


sync_flag_path = os.path.join(output_path, "sync_flag")

def has_sync_happened() -> bool:
    if os.path.exists(sync_flag_path):
        return True
    return False

def set_sync_happened():
    file = open(sync_flag_path, 'w')
    file.write(" ")
    file.close()

