import os
from .gentoomuch_common import kernel_configs_path, kernel_defines_path, kconfigs_mountpoint, output_path

def prep_kernel_config(name: str):
    specific_kernel_defines_path = os.path.join(kernel_defines_path, name)
    specific_kernel_defines_config_path = os.path.join(specific_kernel_defines_path, 'config')
    specific_kernel_defines_sources_path = os.path.join(specific_kernel_defines_path, 'sources')
    defines_exists = os.path.isdir(specific_kernel_defines_path) and os.path.isfile(specific_kernel_defines_config_path) and os.path.isfile(specific_kernel_defines_sources_path)
    if defines_exists:
        with open(specific_kernel_defines_config_path) as file:
           config_name = file.read().strip()
        with open(specific_kernel_defines_sources_path) as file:
            sources_name = file.read().strip()
        config_filename = config_name + ".kconf"
        host_kconf_path = os.path.join(kernel_configs_path, config_filename)
        mounted_kconf_path = os.path.join(kconfigs_mountpoint, config_filename)
        kernel_path = "/usr/src/linux"
        active_kconf_path = "/usr/src/linux/.config"
        cmd_str = 'emerge --onlydeps ' + sources_name + ' && '
        cmd_str += 'emerge --oneshot --usepkg n ' + sources_name + ' && '
        cmd_str += "cd " + kernel_path + " && "
        kconf_exists = os.path.isfile(host_kconf_path)
        if kconf_exists:
            cmd_str += "cp " + mounted_kconf_path + " " + active_kconf_path + " && "
            cmd_str += "make nconfig && "
            cmd_str += "cp " + active_kconf_path + " " + mounted_kconf_path
            swap_stage(arch, desired_profile, "gentoomuch/builder", False) 
            pass
        else:
            cmd_str += "make nconfig && "
            cmd_str += "cp " + active_kconf_path + " " + mounted_kconf_path
        code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
        if code == 0:
            pass
    else:
        exit("Could not find correct kernel definition in " + specific_kernel_defines_path)