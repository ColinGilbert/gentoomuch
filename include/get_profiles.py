import os
from .gentoomuch_common import profiles_path

def get_profiles():
    results = []
    with open(profiles_path, 'r') as file:
        profiles = file.readlines()
        for p in profiles:
            results.append(p.strip())

    return results