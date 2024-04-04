from fabric.api import *
import os

env.user = 'ubuntu'
env.hosts = ["104.196.155.240", "34.74.146.120"]
env.key_filename = "~/id_rsa"

def do_clean(number=0):
    """Deletes out-of-date archives"""
    try:
        number = int(number)
    except ValueError:
        print("Error: Invalid number argument.")
        return

    local_versions_path = "~/AirBnB_Clone_V2/versions"
    remote_releases_path = "/data/web_static/releases"

    # Get list of local and remote archive files
    local_archives = local("ls -t {}".format(local_versions_path), capture=True).split()
    remote_archives = sudo("ls -t {}".format(remote_releases_path), quiet=True).split()

    # Remove excess local archives
    for archive in local_archives[number:]:
        local("rm -f {}/{}".format(local_versions_path, archive))

    # Remove excess remote archives
    for archive in remote_archives[number:]:
        sudo("rm -rf {}/{}".format(remote_releases_path, archive.strip(".tgz")))

