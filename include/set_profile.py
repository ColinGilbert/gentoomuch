#!/usr/bin/env python3

from .gentoomuch_common import current_profile_path, profiles_amd64

def set_profile(arg):
  if arg in profiles_amd64:
    print("Setting profile to " + arg)
    open(current_profile_path, 'w').write(arg)
  else:
    exit("Invalid profile name: " + arg)