import os
from .gentoomuch_common import output_path, kconfigs_mountpoint
from .swap_stage import swap_stage

def build_kernel(arch, profile, kconfig, jobs):
    print("BUILDING KERNEL " + kconfig)
    kconf_mountpoint = os.path.join(kconfigs_mountpoint, kconfig + '.kconf')
    cmd_str = "cp " + kconf_mountpoint + " /usr/src/linux/.config && "
    cmd_str += "cd /usr/src/linux && "
    #cmd_str += "make clean && "
    #cmd_str += "KBUILD_BUILD_TIMESTAMP='' make CC='ccache gcc' -j" + jobs
    cmd_str += "make -j " + jobs
    swap_stage(arch, profile, "gentoomuch/builder", upstream = False)
    code = os.system("cd " + output_path + ' && docker-compose run gentoomuch-builder /bin/bash -c "' + cmd_str + '"')
    if code == 0:
        return True
    else:
        return False