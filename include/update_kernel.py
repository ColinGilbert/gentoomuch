    #!/usr/bin/env python3
import os
from .gentoomuch_common import output_path
from .swap_stage import swap_stage
from .get_desired_profile import get_desired_profile

def update_kernel(arch :str):
    print("UPDATING KERNEL")
    profile = get_desired_profile()
    if profile == '':
        exit("You need to set a desired profile.")
    swap_stage(arch, profile, "gentoomuch-builder", False) 
    code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c 'rm -rf /usr/src/* && emerge -q gentoo-sources'")
    if code == 0:
        pass