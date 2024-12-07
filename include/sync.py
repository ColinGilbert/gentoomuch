#!/usr/bin/env python3

import os
from .gentoomuch_common import output_path
from .get_gentoomuch_uid import get_gentoomuch_uid

def sync():
    squashed_path = '/mnt/squashed-portage/portage.squash'
    os.system("cd " + output_path + " && docker-compose run gentoomuch-updater /bin/bash -c 'rm " + squashed_path + " & emerge -v --sync && emerge squashfs-tools && mksquashfs /var/db/repos/gentoo " + squashed_path + " -noappend -force-gid portage -force-uid portage && chown " + get_gentoomuch_uid() +  ":" + get_gentoomuch_uid() + ' ' + squashed_path + "'")


sync_flag_path = os.path.join(output_path, "sync_flag")

def has_sync_happened() -> bool:
    if os.path.exists(sync_flag_path):
        return True
    return False

def set_sync_happened():
    file = open(sync_flag_path, 'w')
    file.write(" ")
    file.close()