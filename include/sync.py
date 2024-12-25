#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path, squashed_ports_mounted_filepath
from .create_composefile import create_composefile
from .get_gentoomuch_uid import get_gentoomuch_uid
from .get_gentoomuch_gid import get_gentoomuch_gid

def sync():
    print("GENTOOMUCH: Syncing Portage. This may take some time...")
    cmd_str = 'emerge -v --sync && '
    cmd_str += 'emerge --oneshot squashfs-tools && '
    cmd_str += 'rm -f ' + squashed_ports_mounted_filepath + ' && '
    cmd_str += 'mksquashfs /var/db/repos/gentoo ' + squashed_ports_mounted_filepath + ' && '
    cmd_str += 'chown ' + get_gentoomuch_uid() + ':' + get_gentoomuch_gid() + ' ' + squashed_ports_mounted_filepath
    code = os.system("cd " + output_path + " && docker-compose run gentoomuch-updater /bin/bash -c '" + cmd_str + "'")
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

