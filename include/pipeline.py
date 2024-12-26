import os
from .gentoomuch_common import stage4_defines_path
from .clean_kernel_sources import clean_kernel_sources
from .get_desired_profile import get_desired_profile
from .build_stage4 import build_stage4

def pipeline(arch: str):
    # Get all stage 4 definitions
    stage4s = []
    for s in os.listdir(stage4_defines_path):
        print(s)
        #if os.path.isdir(s):
        #print("Found stage4: " + s)
        stage4s.append(s)
    #print("stage4s: " + str(stage4s))
    # Then, put them all in a list: [(kconfig, name, profile, stage3)]
    #TODO: Sort them by kernel config
    stage4_list = []
    for stage4_name in stage4s:
        build_stage4(arch, stage4_name)
        if not valid:
            print("PIPELINE BROKEN TRYING TO SAVE: " + stage4_name)
            return False
    #clean_kernel_sources(arch, get_desired_profile())
    return True