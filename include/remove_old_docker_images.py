import os, docker

def remove_old_docker_images():
    dkr = docker.from_env()
    images = dkr.images.list()
    for i in images:
        if len(i.tags) == 0:
            dkr.images.remove(i.id, True, False)
        else:
            for t in i.tags:
                if t.split('/')[1].split(':')[1] == 'upstream':
                    dkr.images.remove(i.id, True, False)