#!/usr/bin/env python3

import docker
from .get_docker_tag import get_docker_tag


def docker_stage_exists(arch, profile, stagedef, upstream: bool) -> bool:
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    t = get_docker_tag(arch, profile, stagedef, bool(upstream))
    for i in dckr_imgs:
        if t in i.tags:
            return True
    return False
