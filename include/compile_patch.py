import os
from .gentoomuch_common import output_path, portage_output_path
from .package_from_patch import package_from_patch
from .swap_stage import swap_stage
from .get_arch import get_arch

def compile_patch(profile: str, patch_name : str) -> bool:
    valid, package_name = package_from_patch(patch_name, False)
    if not valid:
        print("PATCH COMPILATION: Invalid patch name entered. Stopping.")
        return False
    patch_outdir = os.path.join(portage_output_path, 'patches')
    cmd_str = 'emerge -q --onlydeps =' + package_name + ' && '
    cmd_str += "emerge -q --usepkg n =" + package_name
    if valid:
        swap_stage(get_arch(), profile, 'gentoomuch-builder', False, patch_name)
        code = os.system("cd " + output_path + " && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
        if code == 0:
            pass
        return True
    print("PATCH COMPILATION: Trying patch " + patch_name + " failed.")
    return False