    #!/usr/bin/env python3
import os
from .gentoomuch_common import output_path
from .swap_stage import swap_stage
from .get_desired_profile import get_desired_profile

def update_kernel(arch :str):
    print("UPDATING KERNEL")
    swap_stage(arch, get_desired_profile(), "gentoomuch-builder", False) 
    code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c 'rm -rf /usr/src/* && emerge gentoo-sources'")
    if code == 0:
        pass