import os
from .gentoomuch_common import kernel_configs_path, kernel_defines_path

def prep_kernel(name: str):
    specific_kernel_defines_path = os.path.join(kernel_defines_path, name)
    specific_kernel_defines_config_path = os.path.join(specific_kernel_defines_path, 'config')
    specific_kernel_defines_sources_path = os.path.join(specific_kernel_defines_path, 'sources')
    defines_exists = os.isdir(specific_kernel_defines_path) and os.isfile(specific_kernel_defines_config_path) and os.isfile(specific_kernel_defines_sources_path)
    if defines_exists:
        with open(specific_kernel_defines_config_path) as file:
           config_name = file.read().strip() 
        kconf_path = os.path.join(kernel_configs_path, config_name + '.kconf')
        kconf_exists = os.isfile(kconf_path)
        if kconf_exists:
            # TODO: copy file to staging area, setup gentoomuch-builder to use kernel-nconfig, save kernel config when done
        else:
            # Setup gentoomuch-builder with kernel-nfconfig, save kernel config when done 

    else:
        exit("Could not find correct kernel definition in " + specific_kernel_defines_path)