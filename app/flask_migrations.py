import os
import subprocess
from subprocess import PIPE

def get_migration_status():
    try:
        heads=subprocess.run("flask db heads", shell=True, check=True, stdout=PIPE)
        heads=heads.stdout
    except subprocess.CalledProcessError:
        heads=None
    try:
        current=subprocess.run("flask db current", shell=True, check=True, stdout=PIPE)
        current=current.stdout
    except subprocess.CalledProcessError:
        current=None
    return heads, current

heads, current = get_migration_status()

if heads is None and current is None:
    subprocess.run("echo feels like new", shell=True, check=True)
    subprocess.run("flask db init", shell=True, check=True)
    subprocess.run("flask db migrate", shell=True, check=True)
    subprocess.run("flask db upgrade", shell=True, check=True)
elif heads is not None and current == b'':
    subprocess.run("echo migrations folder feels stale", shell=True, check=True)
    subprocess.run("rm -rf migrations", shell=True, check=True)
    subprocess.run("flask db init", shell=True, check=True)
    subprocess.run("flask db migrate", shell=True, check=True)
    subprocess.run("flask db upgrade", shell=True, check=True)
else:
    subprocess.run("echo checking for updates", shell=True, check=True)
    subprocess.run("flask db migrate", shell=True, check=True)
    subprocess.run("flask db upgrade", shell=True, check=True)
