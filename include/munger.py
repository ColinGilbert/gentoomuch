#!/usr/bin/env python3

import sys, os, re
from .gentoomuch_common import portage_output_path, config_path, stage3_defines_path, cpu_path, pkgset_path, local_config_basepath, hooks_path, global_config_path, debug
from .read_file_lines import read_file_lines
from .read_by_token import read_by_token
from .write_file_lines import write_file_lines

dont_munge_files = (['', 'bashrc'], ['', 'modules'], ['', 'README.md'], ['', 'mirrors'], ['', 'color.map'])
dont_munge_dirs = ('sets', 'patches', 'savedconfig')


class munger:
    def __init__(self, current_dir, current_file):
        self.use_flags = dict() #[str, Dict[bool, List[str]]] 
        self.unmodified_lines = list()#[] #[str]
        self.atoms = set() # [str]
        self.current_directory = current_dir
        self.current_file = current_file
    
    # This identifies and deduplicates flags
    # It will verify for set/unset combinations and return False upon spotting one.
    # This allows the user to avoid potential surprises.
    def ingest(self, line):
        atom = self.__get_atom_name(line)
        flags_str = re.sub('^' + re.escape(atom), '', line)
        flags_str = self.__strip_quotes(flags_str)
        # Now, we figure out whether or not the line gets passthrough or has its values held into dictionary.
        if self.current_file == "make.conf" and self.current_directory == "" and self.__is_atom_portage_var(atom):
            atom = re.sub('=$', '', atom)
            self.__ingest_use_flags(atom, flags_str)
        elif self.__is_file_pkg_flags_syntax():
            self.__ingest_use_flags(atom, flags_str)
        elif self.__is_file_simple_atom_syntax():
            self.__ingest_atom(atom)
        else:
            self.unmodified_lines.append(line)

    def get_text(self):
        results = []
        for l in self.unmodified_lines:
            results.append(l)
        if self.current_directory == '' and self.current_file == 'make.conf':
            for l in self.__get_text_make_conf_syntax():
                results.append(l + '\n')
        if self.__is_file_pkg_flags_syntax():
            for l in self.__get_text_pkg_flags_syntax():
                results.append(l + '\n')
        if self.__is_file_simple_atom_syntax():
            for l in self.__get_text_simple_atom_syntax():
                results.append(l + '\n')
        return results

    def get_current_directory(self):
        return self.current_directory

    def get_current_filename(self):
        return self.current_file

    # The argument atom refers to the first word in the config file. I do not know whether or not this terminology jives with the Gentoo upstream; I will double-check, as such this method may be renamed.
    def __is_atom_portage_var(self, atom):
        return bool(re.search('^USE', atom)) or bool(re.search('^CPU_FLAGS_', atom)) or bool(re.search('^ACCEPT_', atom)) or bool(re.search('^FEATURES', atom))

    def __is_file_simple_atom_syntax(self):
        files = ('package.mask', 'package.unmask')
        if self.current_directory == '' and self.current_file in files:
            return True
        else:
            return False

    def __is_file_pkg_flags_syntax(self):
        files = ('package.accept_keywords', 'package.use', 'package.env')
        if self.current_directory == 'package.use' or (self.current_directory == '' and self.current_file in files):
            return True
        else:
            return False

    def __get_text_make_conf_syntax(self):
        results = []
        for atom in self.use_flags.keys():
            counter = 0
            line = atom + '="'
            for flag in self.use_flags[atom][True]:
                if counter > 0:
                    line += ' '
                line += flag
                counter += 1
            for flag in self.use_flags[atom][False]:
                if counter > 0:
                    line += ' -'
                else:
                    line += '-'
                line += flag
            line += '"'
            results.append(line)
        return results

    def __get_text_pkg_flags_syntax(self):
        results = []
        for atom in self.use_flags.keys():
            line = atom
            for flag in self.use_flags[atom][True]:
                line += ' '
                line += flag
            for flag in self.use_flags[atom][False]:
                line += ' -'
                line += flag
            results.append(line)
        return results

    def __get_text_simple_atom_syntax(self):
        results = []
        for atom in self.atoms:
            if not atom[0] == '#':
                results.append(atom)
        return results
    
    def __get_atom_name(self, line):
        if not re.match('(\S)+', line): # Only proceed if we don't have an empty line... Those make the regex engine crash
            return ""
        atom_name = re.match('^\S+', self.__strip_quotes(line)).group() # Get the first block of non-whitespace characters
        if atom_name[0] == '#': # Skip comments
            return ""
        else:
            return atom_name

    def __strip_quotes(self, line):
        return re.sub('(\'|")+', ' ', line) # Strip out them quotes!

    def __get_canonical_flagname(self, line): # Get rid of the negative signs in front.
        return re.sub('^(-)+', '', line)

    def __ingest_atom(self, atom):
        if not atom[0] == '#':
            self.atoms.add(atom)
    
    def __ingest_use_flags(self, atom_name, flags_str):
        for candidate_flag in flags_str.split():
            candidate_flag = candidate_flag.strip()
            if candidate_flag[0] == '#': # Skip comments
                break
            if candidate_flag == "" or candidate_flag == '=':
                continue
            if atom_name not in self.use_flags:
                self.use_flags[atom_name] = dict()
                self.use_flags[atom_name][True] = []
                self.use_flags[atom_name][False] = []
            flag_abs = self.__get_canonical_flagname(candidate_flag)
            is_setting = bool(flag_abs == candidate_flag)
            # Now, we actually add (or not) to our dictionary.
            if flag_abs in self.use_flags[atom_name][is_setting]: # If it's already in our list, we can move on. That's how we implement deduplication!
                continue
            elif flag_abs in self.use_flags[atom_name][not is_setting]: # If that flag is in converse list, then adding the opposite flag will only cause confusion.
                return False
            else: # We now can append anything that has passed the previous tests.
                self.use_flags[atom_name][is_setting].append(flag_abs)
        return True
