#!/usr/bin/python3
"""Web server distribution"""

from fabric.api import *
from datetime import datetime
import os

# Define Fabric environment variables
env.user = 'ubuntu'
env.hosts = ["104.196.155.240", "34.74.146.120"]
env.key_filename = "~/id_rsa"


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder"""

    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Generate a timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the archive
    archive_name = "web_static_{}.tgz".format(timestamp)
    local("tar -czvf versions/{} web_static".format(archive_name))

    # Check if the archive was created successfully
    if os.path.exists("versions/{}".format(archive_name)):
        return os.path.abspath("versions/{}".format(archive_name))
    else:
        return None


def do_deploy(archive_path):
    """Deploys the archive to the web servers"""

    # Check if the archive exists
    if not os.path.exists(archive_path):
        print("Error: Archive path does not exist:", archive_path)
        return False

    try:
        # Extract the archive filename
        archive_name = os.path.basename(archive_path)
        base_name = os.path.splitext(archive_name)[0]

        # Upload the archive to the remote server
        put(archive_path, "/tmp/{}".format(archive_name))

        # Create the directory structure
        sudo("mkdir -p /data/web_static/releases/{}/".format(base_name))

        # Unpack the archive
        sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
             .format(archive_name, base_name))

        # Delete the uploaded archive
        sudo("rm /tmp/{}".format(archive_name))

        # Move contents to appropriate location
        sudo("mv /data/web_static/releases/{}/web_static/* "
             "/data/web_static/releases/{}/"
             .format(base_name, base_name))

        # Remove empty directory
        sudo("rm -rf /data/web_static/releases/{}/web_static"
             .format(base_name))

        # Update symbolic link
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current"
             .format(base_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """Automates the deployment process"""
    # Create a new archive
    archive_path = do_pack()

    if not archive_path:
        print("Error: Archive creation failed.")
        return False

    # Deploy the new archive
    return do_deploy(archive_path)


# Entry point of the script
if __name__ == "__main__":
    deploy()

