import os
from .gentoomuch_common import kernel_configs_path, kconfigs_mountpoint, output_path
from .swap_stage import swap_stage

def prep_kernel_config(arch: str, profile: str, kconf: str):
    host_kconf_path = os.path.join(kernel_configs_path, kconf + '.kconf')
    mounted_kconf_path = os.path.join(kconfigs_mountpoint, kconf + '.kconf')
    cmd_str = "cd /usr/src/linux && "
    kconf_exists = os.path.isfile(host_kconf_path)
    if kconf_exists:
        cmd_str += "cp " + mounted_kconf_path + " /usr/src/linux/.config && "
    cmd_str += "make nconfig && "
    cmd_str += "cp /usr/src/linux/.config " + mounted_kconf_path
    swap_stage(arch, profile, stage_define = "gentoomuch/builder", upstream = False) 
    code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
    if code == 0:
        pass