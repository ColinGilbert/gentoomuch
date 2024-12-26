import os
from .get_profiles import get_profiles
from .gentoomuch_common import stage4_defines_path, saved_patches_path
from .save_tarball import save_tarball
from .get_profiles import get_profiles

def build_stage4(arch: str, stage4_name: str):
    path = os.path.join(stage4_defines_path, stage4_name)
    if not os.path.isfile(os.path.join(path, 'kconf')):
        exit("BUILD STAGE4: Stage 4 definition " + stage4_name + " needs a file named 'kconf' with a valid kernel configuration's name in it")
    if not os.path.isfile(os.path.join(path, 'profile')):
        exit("BUILD STAGE4: Stage 4 definition " + + stage4_name + " needs a file named 'profile' with a valid profile's name in it")
    if not os.path.isfile(os.path.join(path, 'stage3')):
        exit("BUILD STAGE4: Stage 4 definition " + stage4_name + " needs a file named 'stage3' with a valid stage3's name in it")
    with open(os.path.join(path, 'kconf')) as file:
        kconf = file.read().strip()
    with open(os.path.join(path, 'profile')) as file:
        profile = file.read().strip()
        if profile not in get_profiles():
            exit("BUILD STAGE4: Need to set a valid profile for " + stage4_name)
    with open(os.path.join(path, 'stage3')) as file:
        stage3_name = file.read().strip()
    scripts = []
    if os.path.isfile(os.path.join(path, 'scripts')):
        with open(os.path.join(path, 'scripts')) as file:
            scripts = file.readlines()        
    removes = []
    if os.path.isfile(os.path.join(path, 'removes')):
        with open(os.path.join(path, 'removes')) as file:
            removes = file.readlines()
    #print("APPENDING " + kconf + ", " + stage4_name + ", " + profile + ", " + stage3_name)
    #stage4_list.append((kconf, stage4_name, profile, stage3_name, scripts, removes))
    # TODO: Once that is done, foreach kernel build it and pack each stage belonging to it. Make sure to rename it to the stage4 definition name
    patches = []
    for p in os.listdir(saved_patches_path):
        if os.path.isdir(p):
            patches.append(p)
    #for (kconfig, stage4_name, profile, stage3_name, scripts, removes) in stage4_list:
    valid, archive_name = save_tarball(arch, profile, stage_define = stage3_name, upstream = False, patches = patches, patches_have_been_compiled = True, kconfig = kconf, friendly_name = stage4_name, custom_stage = stage3_name, scripts = scripts, removes = removes)
    if not valid:
        return False,''
    return True, archive_name
        