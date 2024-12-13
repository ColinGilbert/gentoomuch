#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import stage3_defines_path, desired_stage_path


# This lists stages
def list_stages():
  # Get currently active stage. Indexing by number is not allowed in this tool: indexing would break once a new stage gets defined, leading to user surprises. :(.
    stage_set = False
    if os.path.isfile(desired_stage_path):
        desired = open(desired_stage_path).read().strip()
        stage_set = True
    print("Listing user-defined stages:")
    for dirpath, dirs, files in sorted(os.walk(stage3_defines_path)):
        if not dirs:
            d = os.path.relpath(dirpath, stage3_defines_path)
            if stage_set:
                print((' [*] ' if d == desired else ' [ ] ') + ' ' + d)
            else:
                print(' [ ] ' + d)
