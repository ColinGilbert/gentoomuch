import os
from .gentoomuch_common import output_path, portage_output_path, saved_patches_path
from .create_composefile import create_composefile

def apply_saved_patches():
    dirs = os.listdir(saved_patches_path)
    patch_outdir = os.path.join(portage_output_path, 'patches')
    code = os.system('mkdir -p ' + patch_outdir + ' & rm -rf ' + os.path.join(patch_outdir, '*'))
    if code == 0:
        pass
    # print("APPLYING SAVED PATCHES... ")
    for d in dirs:
        if d == 'README.md':
            continue
        code = os.system('rsync -aH ' + os.path.join(saved_patches_path, d, '*') + ' ' + patch_outdir)
        if code == 0:
            pass
    #create_composefile(output_path)