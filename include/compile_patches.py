import os
from .get_profiles import get_profiles
from .swap_stage import swap_stage
from .package_from_patch import package_from_patch


def compile_patches(arch: str, patches: [str]):
    profiles = get_profiles()
    for profile in profiles:
        swap_stage(arch, profile, 'gentoomuch-builder')
        for patch in patches:
            valid, package = package_from_patch(patch)
            if valid:
                cmd_str = "emerge -j" + jobs + " --oneshot --onlydeps =" + package + " && "
                cmd_str += "emerge -j" + jobs + " --oneshot --usepkg n =" + package + " && "
                code = os.system('docker-compose run gentoomuch-builder /bin/bash -c "' + cmd_str + '"')
                if code != 0:
                    print("COMPILE PATCHES: Failed to compile " + package)
                    return False
            else:
                print("COMPILE PATCHES: Unrecognized patch: " + patch)
                return False
    return True