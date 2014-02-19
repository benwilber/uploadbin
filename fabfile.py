import os

from fabric.api import *

env.user = "apps"
env.key_filename = "/Users/benw/.ssh/id_rsa-sunspot-io-apps"

env.appdir = os.path.abspath(os.path.dirname(__file__))
env.distdir = os.path.join(env.appdir, "dist")

env.remote_appdir = "/home/apps/uploadbin"

env.roledefs = {
    'prod': ['sunspot.io']
}

def pack(ref):
    with lcd(env.appdir), hide("running"):
        local("git archive --format=tar {ref} > dist/{ref}.tar".format(ref=ref))


def push(ref="HEAD"):
    pack(ref)
    with lcd(env.appdir), hide("running"):
        put("dist/{ref}.tar".format(ref=ref),
            "{remote_appdir}/{ref}.tar".format(remote_appdir=env.remote_appdir, ref=ref))

    stop()

    with cd(env.remote_appdir), hide("running"):
        run("tar mxf {ref}.tar".format(ref=ref))
        run("find . -name '*.pyc' -delete")

    start()

def stop():
    run("supervisorctl stop uploadbin")

def start():
    run("supervisorctl start uploadbin")

def restart():
    run("supervisorctl restart uploadbin")
