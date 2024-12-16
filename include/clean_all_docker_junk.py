import os

def clean_all_docker_junk():
    code = os.system("docker system prune -f")
    if code == 0:
        pass