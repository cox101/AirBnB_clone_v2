#!/usr/bin/python3
"""web server distribution
"""
from fabric.api import local
import os.path
from datetime import datetime


def do_pack():
    """distributes an archive to your web servers
    """
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Generate timestamp for the archive name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the archive
        archive_name = "web_static_{}.tgz".format(timestamp)
        local("tar -czvf versions/{} web_static".format(archive_name))

        # Check if the archive was created successfully
        if os.path.exists("versions/{}".format(archive_name)):
            return os.path.abspath("versions/{}".format(archive_name))
        else:
            return None
    except Exception as e:
        print("Error packing archive:", e)
        return None

