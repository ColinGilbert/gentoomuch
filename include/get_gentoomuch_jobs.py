#!/usr/bin/env python3

import os
from .gentoomuch_common import env_settings_path

def get_gentoomuch_jobs() -> str:
    jobs_path = os.path.join(env_settings_path, 'jobs')
    if not os.path.isfile(jobs_path):
        exit("You need a jobs file with the number of compile jobs in it at: " + jobs_path)
    with open(jobs_path, 'r') as file:
        jobs = file.read().strip() 
    if not jobs.isnumeric():
        exit("ERROR: jobs needs to be a number!")
    return jobs