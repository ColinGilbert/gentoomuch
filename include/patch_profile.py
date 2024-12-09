#!/usr/bin/env python3

import os, shutil
from .gentoomuch_common import output_path, portage_output_path, image_tag_base, active_image_tag, desired_packages_path, desired_hooks_path, output_path, topatch_config_path, saved_patches_path, patches_output_path
from .read_file_lines import read_file_lines


def patch_profile(profile):
    p = os.path.join(topatch_config_path, profile)
    if os.path.isfile(p):
        for candidate in read_file_lines(p):
            candidate = candidate.strip()
            candidate_dir = os.path.join(saved_patches_path, candidate)
            print("Seeking patch " + candidate + " from : " + candidate_dir)
            if os.path.exists(candidate_dir):
                final_patches_output = os.path.join(patches_output_path, candidate)
                if os.path.isdir(final_patches_output):
                    code = os.system('rm -rf ' + final_patches_output)
                    if code == 0:
                        pass
                print("Applying patch: " + candidate)
                code = os.system("mkdir -p " + final_patches_output + " && rsync -aHX " + candidate_dir + "/* " + final_patches_output)
                if code == 0:
                    pass
            else:
                exit("Cannot apply nonexistent patch: " + candidate)
