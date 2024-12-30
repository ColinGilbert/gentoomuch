import os
from .gentoomuch_common import output_path, stages_path
from .create_composefile import create_composefile
from .save_tarball import save_tarball
from .containerize import containerize
from .swap_stage import swap_stage
from .are_patches_in_conflict import are_patches_in_conflict

def update_builder(arch: str, profile: str):
    if are_patches_in_conflict():
        exit()
    code = create_composefile(output_path)
    if code:
      pass
    swap_stage(arch, profile, stage_define = 'gentoomuch-builder', upstream = False)
    scripts = []
    scripts_file = os.path.join(stage3_defines_path, 'gentoomuch-builder', 'scripts')
    if os.path.isfile(scripts_file):
        scripts = read_file_lines(scripts_file)
    valid, archive_name = save_tarball(arch, profile, stage_define = "gentoomuch-builder", upstream = False, scripts = scripts)
    if valid:
        results = containerize(os.path.join(stages_path, archive_name), arch, profile, stage_define = 'gentoomuch-builder', upstream = False)
        return results
    else:
        return False