import os, subprocess, time, sys, threading, itertools
from sys import argv

# ANSI escape codes for terminal coloring
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

# a small function to colorize text
def colorize(text, color):
    return color + text + tcolors.RESET

# rotating spinner :D
class Spinner:

    def __init__(self, message, color, delay=0.05):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.color = color
        self.spinner_visible = False
        sys.stdout.write(colorize(message, color))

    def write_next(self):
        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(colorize(next(self.spinner), self.color))
                self.spinner_visible = True
                sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')
                    sys.stdout.write('\r')
                sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write('\r')


# erase the line that was printed last (basically a carriage return function)
def erase(n=1):
    for _ in range(n):
        # sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


# print the --help menu
def helpMenu():
    print(colorize("Usage: ", tcolors.YELLOW_BOLD) + colorize("bit [OPTION] ...\n", tcolors.WHITE))
    print(colorize("An efficient git-cli alternative with power functions to speed your workflow.\n", tcolors.CYAN))
    print(colorize("\tpush, p <commit message>\t\tadd files to repo, commit them, and push", tcolors.GREEN))
    print(colorize("\tinit, i <remote> <commit message>\tinit local repo, connect to remote, add/commit files, and push", tcolors.GREEN))
    print(colorize("\nReport bugs at https://github.com/Rohan-Bansal/Bit/issues.", tcolors.RED))

# process the arguments passed to the tool
def processArgs():

    # push changes
    if argv[1] == "push" or argv[1] == "p":
        if len(argv) > 2:
            try:
                with Spinner("Versioning Files ", tcolors.PURPLE_BOLD):
                    subprocess.check_output(["git", "add", "."])
                    time.sleep(0.25)
                erase()
                with Spinner("Committing ", tcolors.PURPLE_BOLD):
                    subprocess.check_output(["git", "commit", "-m", argv[2]])
                    time.sleep(0.25)
                erase()
                with Spinner("Pushing Changes ", tcolors.PURPLE_BOLD):
                    subprocess.check_call(["git", "push", "origin", "master"], stdout=DEVNULL, stderr=subprocess.STDOUT)
                    time.sleep(0.25)
                erase()
                print(colorize("Done!", tcolors.GREEN_BOLD))
            except:
                print(colorize("Sequence exit due to crash. Fix errors and try again.", tcolors.RED))
        else:
            print(colorize("Error. Please specify a commit message. \n\nExample usage: bit push [message]", tcolors.RED))

    # init repo, then push
    elif argv[1] == "init" or argv[1] == "i":
        if len(argv) > 2:
            if ".git" in argv[2]:
                if len(argv) > 3:
                    try:
                        with Spinner("Initializing Repository ", tcolors.PURPLE_BOLD):
                            subprocess.check_output(["git", "init", "."])
                            subprocess.check_output(["git", "remote", "add", "origin", argv[2]])
                            time.sleep(0.2)
                        erase()
                        with Spinner("Versioning/Committing ", tcolors.PURPLE_BOLD):
                            subprocess.check_output(["git", "add", "."])
                            subprocess.check_output(["git", "commit", "-m", argv[3]])
                            time.sleep(0.2)
                        erase()
                        with Spinner("Versioning/Committing ", tcolors.PURPLE_BOLD):
                            subprocess.check_call(["git", "push", "origin", "master"], stdout=DEVNULL, stderr=subprocess.STDOUT)
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

    # print the help menu
    elif argv[1] == "--help":
        helpMenu()

# program start
if __name__ == "__main__":

    # process only if arguments exist in the first place
    if len(argv) > 1:
        processArgs()
    else:
        print(colorize("Error. Use ", tcolors.RED) + colorize("bit --help", tcolors.RED_BOLD) + colorize(" for correct usage.", tcolors.RED))