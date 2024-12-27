import os
from .gentoomuch_common import saved_patches_path
from .package_from_patch import package_from_patch

def are_patches_in_conflict():
    # Get a list of all patch names
    # For each patch_name:
    #   Get package_info (ie: category/package_name-version)
    #   Checking for existence of package_info first in a dictionary (package_info -> patch_name):
    #     If it exists, print error message with conflicting patch_name and return True
    #     Otherwise, add into the dictionary package_info -> patch_name
    # Return False
    patch_names = os.listdir(saved_patches_path)
    patches_dict = {}
    for patch in patch_names:
        if patch != 'README.md':
            package_info = package_from_patch(patch, False)
            if package_info in patches_dict:
                print("FOUND CONFLICTING PATCHES: " + patch + " CONFLICTS WITH " + patches_dict[package_info])
                return True
            else:
                patches_dict[package_info] = patch
    return False