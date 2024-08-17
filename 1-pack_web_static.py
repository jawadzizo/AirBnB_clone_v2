#!/usr/bin/python3
"""fabfile to pack the web_static direcroty into a tgz file"""

from datetime import datetime
from invoke.context import Context


def do_pack():
    """packs web_static directory in a tgz file"""
    c = Context()
    tar_name = f'web_static_{datetime.now().strftime("%Y%m%d%H%M%S")}.tgz'

    c.run("mkdir -p versions")
    with c.cd("web_static"):
        result = c.run(f"tar -cf {tar_name} *")

    if result.failed:
        return None

    c.run(f"mv web_static/{tar_name} versions")
    full_path = c.run(f"realpath versions/{tar_name}", hide=True)
    index = full_path.stdout.find("versions")
    short_path = full_path.stdout[index:]

    return short_path

do_pack()
