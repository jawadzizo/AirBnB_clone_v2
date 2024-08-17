#!/usr/bin/python3
"""fabfile to pack, send and decompress web_static into remote servers"""
from datetime import datetime
from fabric import Connection
from invoke.context import Context
import re


def do_pack():
    """packs web_static directory in a tgz file"""
    c = Context()
    tar_name = 'web_static_{}.tgz'.format(datetime.now().strftime("%Y%m%d%H%M%S"))

    c.run("mkdir -p versions")
    with c.cd("web_static"):
        if c.run(f"tar -cf {tar_name} *").failed:
            return None

    c.run("mv web_static/{} versions".format(tar_name))
    full_path = c.run("realpath versions/{}".format(tar_name), hide=True)
    index = full_path.stdout.find("versions")
    short_path = full_path.stdout[index:]

    return short_path


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


def deploy():
    """packs web static, and then sends it to the remote servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
