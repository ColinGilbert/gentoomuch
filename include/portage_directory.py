#!/usr/bin/env python3

import sys, os 
from .gentoomuch_common import portage_output_path, config_path, stage_defines_path, cpu_path, pkgset_path, local_config_basepath, hooks_path, global_config_path
from .read_file_lines import read_file_lines
from .write_file_lines import write_file_lines
from .munger import munger


class portage_directory:
    def __init__(self):
        self.accumulators = dict() #[str, munger]

    def ingest(self, local_path : str):
        for (dirpath, dirnames, filenames) in os.walk(local_path):
            current_path = os.path.relpath(dirpath, local_path)
            for d in dirnames:
                outdir = os.path.join(portage_output_path, d)
                if not os.path.isdir(outdir):
                   os.mkdir(outdir)
            for f in filenames:
                if f[0] != '.':
                    current_path = os.path.relpath(dirpath, local_path)
                    current_file = os.path.join(current_path, f)
                    if not current_file in self.accumulators: # Add a munger object to prevent a crash
                        self.accumulators[current_file] = munger(current_path, f)
                    for line in read_file_lines(os.path.join(dirpath, f)): # Here we do our actual file-reading
                        self.accumulators[current_file].ingest(line)
                        # sys.exit('portage_directory.setup() - ERROR - Could not ingest ' + current_file + ' due to line : ' + line)


    def writeout(self):
        for m in self.accumulators.values():
            current_output_dir = os.path.join(portage_output_path, m.get_current_directory())
            if not os.path.isdir(current_output_dir):
                os.mkdir(current_output_dir)
            current_output_file = os.path.join(current_output_dir, m.get_current_filename())
            if not os.path.isfile(current_output_file):
                text = m.get_text()
                if len(text) > 0:
                    write_file_lines(current_output_file, text)
