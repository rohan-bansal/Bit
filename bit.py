import os, subprocess, argparse, time, webbrowser
from lib.tcolors import tcolors
from lib.spinner import Spinner
from lib.textlib import colorize, getRandomPhrase, erase

path = os.getcwd()

def error(message):
    print(colorize("err: " + message, tcolors.RED_BOLD))

def getOriginURL():
    try:
        currentBranch = subprocess.check_output(['git', 'branch', '--show-current'],
            stderr=subprocess.STDOUT, encoding='UTF-8').strip()
    except subprocess.CalledProcessError:
        error("is the CWD a git repository?")
        return None
    return currentBranch

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
    currentBranch = getOriginURL()
    if currentBranch == None: return
    
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

def pushChanges(commitBeforePush=False, forcePush=False):
    currentBranch = getOriginURL()
    if currentBranch == None: return

    if commitBeforePush:
        commitChanges()

    print(colorize("pushing local " + currentBranch + " to remote", tcolors.GREEN_BOLD))

    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            if forcePush:
                toForceOrNotToForce = input(colorize("confirm force push [y/n]:  ", tcolors.YELLOW))
                if not toForceOrNotToForce:
                    erase()
                    error("aborted.")
                    return
                subprocess.check_output(["git", "push", "origin", currentBranch, "--force"],
                    stderr=subprocess.STDOUT)
            else:
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

def printRemote():
    try:
        url = str(subprocess.check_output(["git", "config", "--get", "remote.origin.url"], stderr=subprocess.STDOUT), encoding='UTF-8').strip()
        print(colorize(url, tcolors.GREEN))
    except subprocess.CalledProcessError:
        error("no remote url set.")

def pullChanges():
    currentBranch = getOriginURL()
    if currentBranch == None: return

    print(colorize("pulling changes from origin " + currentBranch, tcolors.GREEN_BOLD))

    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "pull", "origin", currentBranch],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            erase();
            if "conflict" in str(e.output):
                error("merge conflicts, please fix before pulling again.")
            else:
                error("action failed for unknown reasons.")
            return
        time.sleep(0.5)

    print(colorize("done.", tcolors.GREEN_BOLD))

def fetchChanges():
    print(colorize("fetching all remote changes", tcolors.GREEN_BOLD))
    
    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "fetch", "--all"],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            error("action failed for unknown reasons.")
            return
        time.sleep(0.5)

    print(colorize("done.", tcolors.GREEN_BOLD))


def switchBranch(branch):
    print(colorize("switching to branch: " + branch, tcolors.GREEN_BOLD))

    branchExists = True

    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "checkout", branch], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            erase()
            branchExists = False
            
        time.sleep(0.5)

    if branchExists:
        print(colorize("done.", tcolors.GREEN_BOLD))
        return
 
    response = input(colorize("branch does not exist. create? [y/n]: ", tcolors.YELLOW))
    if response == "n":
        error("aborted.")
        return
    
    print(colorize("creating new branch: " + branch, tcolors.GREEN_BOLD))
    with Spinner(" ", tcolors.CYAN_BOLD):
        try:
            subprocess.check_output(["git", "checkout", "-b", branch], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            erase()
            error("could not create a new branch.")
        time.sleep(0.5)
    
    print(colorize("done.", tcolors.GREEN_BOLD))

def createNewRepo():
    webbrowser.open('https://github.com/new')

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

create = subparser.add_parser('create')
create.add_argument("-m", type=str, help="specify commit message", required=False)

commit = subparser.add_parser('commit')
commit.add_argument("-m", type=str, help="specify commit message", required=False)

push = subparser.add_parser('push')
push.add_argument("-c", action="store_true", help="commit before push", required=False)
push.add_argument("-f", action="store_true", help="force push", required=False)

origin = subparser.add_parser('origin')
origin.add_argument("-s", type=str, help="origin remote url", required=False)

pull = subparser.add_parser('pull')

fetch = subparser.add_parser('fetchall')

newrepo = subparser.add_parser('newrepo')

checkout = subparser.add_parser('checkout')
checkout.add_argument("branch", type=str, help="branch to checkout")

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
    pushChanges(commitBeforePush=(args.c), forcePush=(args.f))
elif args.command == 'origin':
    if(args.s != None):
        changeRemote(args.s)
    else:
        printRemote()
elif args.command == 'pull':
    pullChanges()
elif args.command == 'fetchall':
    fetchChanges()
elif args.command == 'checkout':
    switchBranch(args.branch)
elif args.command == 'newrepo':
    createNewRepo()
else:
    error("specify a command. (--help)")