import os, git
from .gentoomuch_common import output_path, portage_output_path, patches_workdir
from .package_from_patch import package_from_patch
from .swap_stage import swap_stage
from .get_arch import get_arch

def try_patch(profile: str, patch_name : str) -> bool:
    valid, versioned_package = package_from_patch(patch_name, from_workdir = True)
    if not valid:
        print("PATCH COMPILATION: Invalid patch name entered. Stopping.")
        return False
    patch_outdir = os.path.join(portage_output_path, 'patches')
    base_path = os.path.join(patches_workdir, patch_name, versioned_package)
    for d in os.listdir(base_path):
        print(d)
    final_path = os.path.join(base_path, d)
    repo = git.Repo(final_path)
    # Get first commit.
    first_commit = list(repo.iter_commits('master'))[-1]
    cmd_str = 'cd ' + final_path + ' && '
    cmd_str += "git diff " + first_commit.hexsha + " | grep -v '^diff\|^index' | tee ." + patch_name + ".patch && "
    cmd_str += 'mkdir -p ' + os.path.join(patch_outdir, versioned_package) + ' && '
    cmd_str += 'cp ' + os.path.join(final_path, '.' + patch_name +'.patch') + ' ' + os.path.join(patch_outdir, versioned_package, patch_name + '.patch')
    code = os.system(cmd_str)
    if code != 0:
        print("TRY PATCH: Could not copy patch to portage outputs directory")
        return False
    cmd_str = 'emerge -q --onlydeps =' + versioned_package + ' && '
    cmd_str += "emerge -q --usepkg n =" + versioned_package
    swap_stage(get_arch(), profile, 'gentoomuch-builder', False, str(patch_name))
    code = os.system("cd " + output_path + " && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
    if code == 0:
        pass
        return True
    print("PATCH COMPILATION: Trying patch " + patch_name + " failed.")
    return False