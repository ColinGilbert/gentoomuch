import os, shutil, git
from .gentoomuch_common import saved_patches_path, patches_workdir
from .package_from_patch import package_from_patch

def save_patch(patch_name : str) -> bool:
    p = os.path.join(saved_patches_path, patch_name)
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok = True)
    valid, versioned_package = package_from_patch(patch_name, from_workdir = True)
    if not valid == True:
        print("SAVE PATCH: Could not derive package name") 
        return False
    print("SAVE PATCH: " + versioned_package)
    base_path = os.path.join(patches_workdir, patch_name, versioned_package)
    for d in os.listdir(base_path):
        print(d)
    final_path = os.path.join(base_path, d)
    print("PATCH PATH: " + final_path)
    repo = git.Repo(final_path)
    # Get first commit.
    first_commit = list(repo.iter_commits('master'))[-1]
    num_backtracks = len(versioned_package.split('/'))
    final_output_dir = os.path.join(p, versioned_package)
    os.system("cd " + final_path + " && git diff " + first_commit.hexsha + " | grep -v '^diff\|^index' | tee ." + patch_name + ".patch")
    if os.path.isdir(final_output_dir) and len(os.listdir(final_output_dir)) > 0:
        print("While saving the patch, another directory was found and it is not empty!")
        os.system('rm -rf ' + os.path.join(final_output_dir,'*'))
    os.makedirs(final_output_dir, exist_ok = True)
    shutil.move(os.path.join(final_path, '.' + patch_name + '.patch'), os.path.join(final_output_dir,  patch_name + '.patch'))
    return True
