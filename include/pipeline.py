import os
from .get_profiles import get_profiles
from .gentoomuch_common import stage4_defines_path, saved_patches_path
from .save_tarball import save_tarball
from .get_profiles import get_profiles
from .clean_kernel_sources import clean_kernel_sources
from .get_desired_profile import get_desired_profile

def pipeline(arch: str):
    # Get all stage 4 definitions
    stage4s = []
    for s in os.listdir(stage4_defines_path):
        print(s)
        #if os.path.isdir(s):
        #print("Found stage4: " + s)
        stage4s.append(s)
    #print("stage4s: " + str(stage4s))
    # Then, sort them all by kconfig in a list: [(kconfig, name, profile, stage3)]
    stage4_list = []
    for stage4_name in stage4s:
        path = os.path.join(stage4_defines_path, stage4_name)
        if not os.path.isfile(os.path.join(path, 'kconf')):
            exit("PIPELINE: Stage 4 definition " + stage4_name + " needs a file named 'kconf' with a valid kernel configuration's name in it")
        if not os.path.isfile(os.path.join(path, 'profile')):
            exit("PIPELINE: Stage 4 definition " + + stage4_name + " needs a file named 'profile' with a valid profile's name in it")
        if not os.path.isfile(os.path.join(path, 'stage3')):
            exit("PIPELINE: Stage 4 definition " + stage4_name + " needs a file named 'stage3' with a valid stage3's name in it")
        with open(os.path.join(path, 'kconf')) as file:
            kconf = file.read().strip()
        with open(os.path.join(path, 'profile')) as file:
            profile = file.read().strip()
            if profile not in get_profiles():
                exit("PIPELINE: Need to set a valid profile for " + stage4_name)
        with open(os.path.join(path, 'stage3')) as file:
            stage3_name = file.read().strip()
        #print("APPENDING " + kconf + ", " + stage4_name + ", " + profile + ", " + stage3_name)
        stage4_list.append((kconf, stage4_name, profile, stage3_name))
    # TODO: Once that is done, foreach kernel build it and pack each stage belonging to it. Make sure to rename it to the stage4 definition name
    patches = []
    for p in os.listdir(saved_patches_path):
        if os.path.isdir(p):
            patches.append(p)
    for (kconfig, stage4_name, profile, stage3_name) in stage4_list:
        #def save_tarball(arch: str, profile: str, stage_define: str, upstream: bool, patches: [str] = [], patches_have_been_compiled: bool = True, kconfig: str = '', emerge_kernel: bool = False, strip_deps = bool: False, friendly_name : str = ''):
        (valid, archive_name) = save_tarball(arch, profile, stage_define = stage3_name, upstream = False, patches = patches, patches_have_been_compiled = True, kconfig = kconf, emerge_kernel = False, strip_deps = True, friendly_name = stage4_name)
        if not valid:
            print("PIPELINE BROKEN TRYING TO SAVE: " + stage4_name)
            return False
    clean_kernel_sources(arch, get_desired_profile())
    return True