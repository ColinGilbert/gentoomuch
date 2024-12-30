import os
from .get_profiles import get_profiles
from .gentoomuch_common import stage3_defines_path, saved_patches_path, output_path, stages_path
from .save_tarball import save_tarball
from .get_profiles import get_profiles
from .are_patches_in_conflict import are_patches_in_conflict
from .create_composefile import create_composefile
from .containerize import containerize
from .swap_stage import swap_stage
from .sync import set_sync_happened, has_sync_happened
from .read_file_lines import read_file_lines

def bootstrap_builder(arch: str, profile: str, tarball_path: str ):
    if are_patches_in_conflict():
        exit()
    code = create_composefile(output_path)
    if code:
      pass
    code = containerize(tarball_path, arch, profile, stage_define = '', upstream = True)
    if not code:
        exit("Failed to load tarball")
    if not has_sync_happened():
        print("Syncing for first time!")
        swap_stage(arch, profile, stage_define = 'gentoomuch-builder', upstream = True)
        code = sync()
        if code != 0:
            exit("Could not sync")
        else:
            set_sync_happened()
    scripts = []
    scripts_file = os.path.join(stage3_defines_path, 'gentoomuch-builder', 'scripts')
    if os.path.isfile(scripts_file):
        scripts = read_file_lines(scripts_file)
    valid, archive_name = save_tarball(arch, profile, stage_define = "gentoomuch-builder", upstream = True, scripts = scripts)
    if valid:
        results = containerize(os.path.join(stages_path, archive_name), arch, profile, stage_define = 'gentoomuch-builder', upstream = False)
        return results
    else:
        return False