import os
from .gentoomuch_common import patches_workdir 

def package_from_patch(patch_name : str) -> bool:
    if patch_name == '':
        return (False, '')
    patch_in_progress = os.path.join(patches_workdir, patch_name)
    if len(os.listdir(patch_in_progress)) > 0:
        package_class_name = os.listdir(patch_in_progress)[0]
        package_class_path = os.path.join(patch_in_progress, package_class_name)
        if len(os.listdir(package_class_path)) > 0:
            package_atom_name = os.listdir(package_class_path)[0]
            candidate = package_class_name + '/' + package_atom_name
            return (True, candidate)
        else:
            return (False, '')
    else:
        return (False, '')