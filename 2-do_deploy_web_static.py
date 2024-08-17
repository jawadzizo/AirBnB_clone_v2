#!/usr/bin/python3
"""fabfile to unpack the web_static archive into the remote servers"""

from fabric import Connection
from invoke.context import Context
import re


def do_deploy(archive_path):
    """deploys static files archive into remote servers"""
    l = Context()
    if l.run(f"test -f {archive_path}").failed:
        return False

    i = re.search("web_static_\d{14}\.tgz", archive_path)
    archive_name = archive_path[i.start():]
    decompression_path = f"/data/web_static/releases/{archive_name[:-4]}"

    hosts = ("34.203.33.120", "54.167.185.108")

    for host in hosts:
        remote = Connection(host=host)

        remote.put(archive_path, remote="/tmp/")
        if remote.run(f"mkdir -p {decompression_path}").failed:
            return False
        if remote.run(f"tar -xzf /tmp/{archive_name} -C {decompression_path}").failed:
            return False
        if remote.run(f"rm /tmp/{archive_name}").failed:
            return False
        if remote.run("rm /data/web_static/current").failed:
            return False
        if remote.run(f"ln -s {decompression_path} /data/web_static/current").failed:
            return False

    return True
