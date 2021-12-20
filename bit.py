import os, sys, subprocess, argparse, time
from lib.tcolors import tcolors
from lib.spinner import Spinner
from lib.textlib import colorize, getRandomPhrase, erase

path = os.getcwd()

def error(message):
    print(colorize("err: " + message, tcolors.RED_BOLD))

def createRepo(message="initial commit"):
    print(colorize("initializing repository in ", tcolors.GREEN_BOLD) + colorize(path, tcolors.CYAN))

    if os.path.exists(os.path.join(path, '.git')):
        response = input(colorize("git repository already exists. reinitialize? [y/n]: ", tcolors.YELLOW))
        if response == 'n':
            error('aborted.')
            return
        
    with Spinner(" ", tcolors.CYAN_BOLD):
        subprocess.check_output(["git", "init", "."], 
            stderr=subprocess.STDOUT)
        subprocess.check_output(["git", "add", "."],
            stderr=subprocess.STDOUT)
        try:
            subprocess.check_output(["git", "commit", "-m", message])
        except subprocess.CalledProcessError:
            pass
        time.sleep(0.5)

    print(colorize("done.", tcolors.GREEN_BOLD))

def commitChanges(promptMessage=None):
    try:
        currentBranch = subprocess.check_output(['git', 'branch', '--show-current'],
            stderr=subprocess.STDOUT, encoding='UTF-8').strip()
    except subprocess.CalledProcessError:
        error("is the CWD a git repository?")
        return
    
    print(colorize("committing changes to " + currentBranch, tcolors.GREEN_BOLD))

    if promptMessage == None:
        promptMessage = input(colorize("commit message [enter for random]: ", tcolors.YELLOW))
        if promptMessage == "":
            promptMessage = getRandomPhrase()
    
    with Spinner(" ", tcolors.CYAN_BOLD):
        subprocess.check_output(["git", "add", "."],
            stderr=subprocess.STDOUT)
        time.sleep(0.7)

    try:
        subprocess.check_call(["git", "commit", "-m", promptMessage])
    except subprocess.CalledProcessError:
        pass

    print(colorize("done.", tcolors.GREEN_BOLD))

def pushChanges(commitBeforePush=False):
    try:
        currentBranch = subprocess.check_output(['git', 'branch', '--show-current'],
            stderr=subprocess.STDOUT, encoding='UTF-8').strip()
    except subprocess.CalledProcessError:
        error("is the CWD a git repository?")
        return

    if commitBeforePush:
        commitChanges()

    print(colorize("pushing local " + currentBranch + " to remote", tcolors.GREEN_BOLD))

    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "push", "origin", currentBranch],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            erase();
            if "git pull" in str(e.output):
                error("mismatched repositories, pull first.")
            else:
                error("is local repository connected to remote?")
            return
        time.sleep(0.5)

    print(colorize("done.", tcolors.GREEN_BOLD))

def changeRemote(remote):
    print(colorize("setting origin URL to ", tcolors.GREEN_BOLD) + colorize(remote, tcolors.CYAN))

    originExists = True

    try:
        subprocess.check_output(["git", "config", "--get", "remote.origin.url"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        originExists = False

    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "remote", "set-url" if originExists else "add", "origin", remote],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            erase();
            error("action failed")
            return
        time.sleep(0.5)

    print(colorize("done.", tcolors.GREEN_BOLD))

def pullChanges():
    try:
        currentBranch = subprocess.check_output(['git', 'branch', '--show-current'],
            stderr=subprocess.STDOUT, encoding='UTF-8').strip()
    except subprocess.CalledProcessError:
        error("is the CWD a git repository?")
        return

    print(colorize("pulling changes from origin " + currentBranch, tcolors.GREEN_BOLD))

    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "pull", "origin", currentBranch],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            erase();
            if "conflict" in e.output:
                error("merge conflicts, please fix before pulling again.")
            else:
                error("action failed for unknown reasons.")
            return
        time.sleep(0.5)

    print(colorize("done.", tcolors.GREEN_BOLD))



parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

create = subparser.add_parser('create')
create.add_argument("-m", type=str, help="specify commit message", required=False)

commit = subparser.add_parser('commit')
commit.add_argument("-m", type=str, help="specify commit message", required=False)

push = subparser.add_parser('push')
push.add_argument("-c", action="store_true", help="commit before push", required=False)

origin = subparser.add_parser('origin')
origin.add_argument("-s", type=str, help="origin remote url", required=True)

pull = subparser.add_parser('pull')

args = parser.parse_args()

if args.command == 'create':
    if(args.m != None):
        createRepo(args.m)
    else:
        createRepo()
elif args.command == 'commit':
    if(args.m != None):
        commitChanges(args.m)
    else:
        commitChanges()
elif args.command == 'push':
    if(args.c != None):
        pushChanges(args.c)
    else:
        pushChanges()
elif args.command == 'origin':
    if(args.s != None):
        changeRemote(args.s)
elif args.command == 'pull':
    pullChanges()
else:
    error("specify a command. (--help)")