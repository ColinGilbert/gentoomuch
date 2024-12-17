import os
from .gentoomuch_common import output_path
from .swap_stage import swap_stage

def clean_kernel_sources(arch, profile):
    print("CLEANING KERNEL SOURCES")
    cmd_str += "cd /usr/src/linux && "
    cmd_str += "make clean"
    swap_stage(arch, profile, "gentoomuch/builder", upstream = False)
    code = os.system("cd " + output_path + ' && docker-compose run gentoomuch-builder /bin/bash -c "' + cmd_str + '"')
    if code == 0:
        return True
    else:
        return False