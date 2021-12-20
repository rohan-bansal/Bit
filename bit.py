import os, sys, subprocess, argparse, time
from lib.tcolors import tcolors
from lib.spinner import Spinner
from lib.textlib import colorize, getRandomPhrase

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



parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

create = subparser.add_parser('create')
create.add_argument("-m", type=str, required=False)

push = subparser.add_parser('commit')
push.add_argument("-m", type=str, required=False)

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