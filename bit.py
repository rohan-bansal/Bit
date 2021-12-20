import os, sys, subprocess
from lib.tcolors import tcolors
from lib.spinner import Spinner
from lib.colorizer import colorize


def createRepo():
    print(tcolors.GREEN + "Creating a new repo..." + tcolors.RESET)
    subprocess.call(["git", "init"])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "Initial commit"])
    print(tcolors.GREEN + "Repo created!" + tcolors.RESET)

def processArgs(arg):
    

    if arg[1] == "--create":
        createRepo();

if __name__ == "__main__":

  processArgs(sys.argv);