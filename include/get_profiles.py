import os
from .gentoomuch_common import profiles_path

def get_profiles():
    profiles = []
    with open(profiles_path, 'r') as file:
        profiles = file.readlines()
    return profiles