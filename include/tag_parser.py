#!/usr/bin/env python3

import re, docker
from .gentoomuch_common import image_tag_base, active_image_tag
from .get_profiles import get_profiles


class tag_parser:

    def __init__(self):
        self.arch = ''
        self.profile = ''
        self.stage_define = ''
        self.upstream = False

    def parse(self, tag):
        self.arch = ''
        self.profile = ''
        self.stage_define = ''
        self.upstream = False
        # If we are dealing with localhost:5000/gentoomuch-current:latest
        if tag == active_image_tag:
            return
        # STATE OF INPUT:
        # A) localhost:5000/gentoomuch-amd64-musl-hardened:upstream
        # B) localhost:5000/gentoomuch-amd64-musl-hardened-custom-memalloc-test:latest
        tag = re.sub(re.escape(image_tag_base), '', tag)
        # STATE OF INPUT:
        # A) amd64-musl-hardened:upstream
        # B) amd64-musl-hardened-custom-memalloc-test:latest
        self.arch = tag[:tag.find('-')] # amd64
        tag = tag[tag.find('-') + 1:] # We strip off "amd64-" 
        # STATE OF INPUT:
        # A) musl-hardened:upstream
        # B) musl-hardened-custom-memalloc-test:latest
        suffix = tag[tag.rfind(':') + 1:] # A) upstream B) latest
        self.upstream = bool(suffix == 'upstream') # We set upstream to True.
        tag = tag[:tag.rfind(':')] # We strip off the suffix tag ":upstream" or ":latest" or whatever. 
        # STATE OF INPUT:
        # A) musl-hardened
        # B) musl-hardened-custom-memalloc-test
        profile_found = False # We start searching within our set of profiles. These are defined in gentoomuch_common.py
        for p in get_profiles(): 
            if tag.startswith(p): # If we match, we can set our data and break out.
                self.profile = p
                profile_found = True
                break
        if not profile_found: # If no valid profile is found, we can leave now.
            return
        tag = tag[len(self.profile) + 1:] # We strip off "musl-hardened-"
        # STATE OF INPUT:
        # A)
        # B) custom-memalloc-test
        # print(tag)
        self.stage_define = tag # What's left over: A) B) custom-memalloc-test

    def str(self):
        return self.arch + '-' + self.profile + (':upstream' if self.upstream else '-' + self.stage_define + ':latest')

    def arch(self):
        return self.arch

    def profile(self):
        return self.profile

    def stage_define(self):
        return self.stage_define

    def upstream(self):
        return self.upstream
