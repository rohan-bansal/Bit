import os, sys, subprocess, argparse, time
from lib.tcolors import tcolors
from lib.spinner import Spinner
from lib.colorizer import colorize

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



parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

create = subparser.add_parser('create')
create.add_argument("-m", type=str, required=False)

args = parser.parse_args()

if args.command == 'create':
    if(args.m != None):
        createRepo(args.m)
    else:
        createRepo()