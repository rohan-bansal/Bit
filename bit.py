import os, subprocess, time, sys
from sys import argv

class tcolors:
    RESET = "\u001B[0m"
    BLACK = "\u001B[30m"
    RED = "\u001B[31m"
    GREEN = "\u001B[32m"
    YELLOW = "\u001B[33m"
    BLUE = "\u001B[34m"
    PURPLE = "\u001B[35m"
    CYAN = "\u001B[36m"
    WHITE = "\u001B[37m"
    BLACK_BOLD = "\033[1;30m"
    RED_BOLD = "\033[1;31m"
    GREEN_BOLD = "\033[1;32m"
    YELLOW_BOLD = "\033[1;33m"
    BLUE_BOLD = "\033[1;34m"
    PURPLE_BOLD = "\033[1;35m"
    CYAN_BOLD = "\033[1;36m"
    WHITE_BOLD = "\033[1;37m"

def colorize(text, color):
    return color + text + tcolors.RESET

def erase(n=1):
    for _ in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

def helpMenu():
    print(colorize("Usage: ", tcolors.YELLOW_BOLD) + colorize("bit [OPTION] ...\n", tcolors.WHITE))
    print(colorize("An efficient git-cli alternative with power functions to speed your workflow.\n", tcolors.CYAN))
    print(colorize("\tpush, p <commit message>\t\tadd files to repo, commit them, and push", tcolors.GREEN))
    print(colorize("\tinit, i <remote> <commit message>\tinit local repo, connect to remote, add/commit files, and push", tcolors.GREEN))
    print(colorize("\nReport bugs at https://github.com/Rohan-Bansal/Bit/issues.", tcolors.RED))


def processArgs():
    if argv[1] == "push" or argv[1] == "p":
        if len(argv) > 2:
            try:
                print(colorize("Versioning All Files...", tcolors.PURPLE_BOLD))
                subprocess.check_output(["git", "add", "."])
                time.sleep(0.2)
                erase()
                print(colorize("Committing...", tcolors.PURPLE_BOLD))
                subprocess.check_output(["git", "commit", "-m", argv[2]])
                time.sleep(0.2)
                erase()
                print(colorize("Pushing Changes...", tcolors.PURPLE_BOLD))
                subprocess.check_output(["git", "push", "origin", "master"])
                time.sleep(0.2)
                erase()
                print(colorize("Done!", tcolors.GREEN_BOLD))
            except:
                print(colorize("Sequence exit due to crash. Fix errors and try again.", tcolors.RED))
        else:
            print(colorize("Error. Please specify a commit message. \n\nExample usage: bit push [message]", tcolors.RED))
    elif argv[1] == "init" or argv[1] == "i":
        if len(argv) > 2:
            if ".git" in argv[2]:
                if len(argv) > 3:
                    try:
                        print(colorize("Initializing Repository...", tcolors.PURPLE_BOLD))
                        subprocess.check_output(["git", "init", "."])
                        subprocess.check_output(["git", "remote", "add", "origin", argv[2]])
                        time.sleep(0.2)
                        erase()
                        print(colorize("Versioning/Committing...", tcolors.PURPLE_BOLD))
                        subprocess.check_output(["git", "add", "."])
                        subprocess.check_output(["git", "commit", "-m", argv[3]])
                        time.sleep(0.2)
                        erase()
                        print(colorize("Pushing Changes...", tcolors.PURPLE_BOLD))
                        subprocess.check_output(["git", "push", "origin", "master"])
                        time.sleep(0.2)
                        erase()
                        print(colorize("Done!", tcolors.GREEN_BOLD))
                    except:
                        print(colorize("Sequence exit due to crash. Fix errors and try again.", tcolors.RED))
                else:
                    print(colorize("Error. Please specify a commit message, \n\nExample usage: bit init [origin] ['message']", tcolors.RED))
            else:
                print(colorize("Error. The remote was not a valid.", tcolors.RED))
        else:
            print(colorize("Error. Please specify a remote origin. \n\nExample usage: bit init [origin] ['message']", tcolors.RED))
    elif argv[1] == "--help":
        helpMenu()

if __name__ == "__main__":
    if len(argv) > 1:
        processArgs()
    else:
        print(colorize("Error. Use ", tcolors.RED) + colorize("bit --help", tcolors.RED_BOLD) + colorize(" for correct usage.", tcolors.RED))