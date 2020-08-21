import os, subprocess, time, sys, threading, itertools, traceback, platform
from getpass import getpass
from cryptography.fernet import Fernet
from sys import argv
from lib.tcolors import tcolors
from lib.spinner import Spinner
from lib.colorizer import colorize

# get the path of this file
def getPath():
    
    return os.path.dirname(os.path.abspath(__file__))

# TODO load the key generated at first run
def load_key():

    return open(getPath() + "/data/key.key", "rb").read()

# TODO write the password to a file to be used elsewhere (encrypted)
def writePassword(username, password):

    with open(getPath() + "/data/creds.txt", 'a+') as file:
        msg = username + ", " + password + "\n"
        file.write(msg)
    encrypt(getPath() + "/data/creds.txt")



# TODO encrypt the keyfile
def encrypt(filename):

    f = Fernet(load_key())
    
    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)

# TODO decrypt the keyfile
def decrypt(filename):
    f = Fernet(load_key())

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(filename, "wb") as file:
        file.write(decrypted_data)


# erase the line that was printed last (basically a carriage return function)
def erase(n=1):

    for _ in range(n):
        # sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

# check if a .git folder exists in the current directory
def gitFolderExists():
    return os.path.exists(".git")

# update git repo credentials in a directory, using set-url
def updateRepositoryCredentials(username, password):
    url = subprocess.run(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE)
    url = url.stdout.decode('utf-8').replace("\n", "").split("//")
    url[0] += "//"
    url[1] = username + ":" + password + "@" + url[1]
    url_complete = url[0] + url[1]
    subprocess.check_output(["git", "remote", "set-url", "origin", url_complete])

# ask user for credentials, set them, update
def getCreds():
    username = input(colorize("Username: ", tcolors.YELLOW_BOLD))
    password = getpass(colorize("Password: ", tcolors.YELLOW_BOLD))
    with Spinner("Processing Password ", tcolors.PURPLE_BOLD):
        writePassword(username, password) 
        time.sleep(0.5)
    erase()

    norepo = False
    with Spinner("Updating Repository Info ", tcolors.PURPLE_BOLD):
        if gitFolderExists():
            updateRepositoryCredentials(username, password)
        else:
            norepo = True
        time.sleep(0.9)  
    erase()

    if norepo == True:
        print(colorize("Git repository does not exist in this directory.", tcolors.RED_BOLD))
    else:
        print(colorize("Credentials Set!", tcolors.GREEN_BOLD))


# print the --help menu
def helpMenu():
    print(colorize("Usage: ", tcolors.YELLOW_BOLD) + colorize("bit [OPTION] ...\n", tcolors.WHITE))
    print(colorize("An efficient git-cli alternative with power functions to speed your workflow.\n", tcolors.CYAN))
    print(colorize("\tpush, p <commit message>\t\tadd files to repo, commit them, and push", tcolors.GREEN))
    print(colorize("\tinit, i <remote> <commit message>\tinit local repo, connect to remote, add/commit files, and push", tcolors.GREEN))
    print(colorize("\tclone, c <remote>\t\t\tclone repository and cd into it afterwards", tcolors.GREEN))
    print(colorize("\tpass, w\t\t\t\t\tset username/password of git repo manually in current directory", tcolors.GREEN))
    print(colorize("\nReport bugs at https://github.com/Rohan-Bansal/Bit/issues.", tcolors.RED))


# initialize repository, with option to ignore git init if folder exists
def initRepo(localInit=True):
    
    if len(argv) > 2:
        if ".git" in argv[2]:
            if len(argv) > 3:
                try:
                    if localInit == True:
                        with Spinner("Initializing Repository ", tcolors.PURPLE_BOLD):
                            subprocess.check_output(["git", "init", "."])
                            subprocess.check_output(["git", "remote", "add", "origin", argv[2]])
                            time.sleep(0.2)
                        erase()
                        if subprocess.run(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE).stdout.decode('utf-8').count(':') == 1:
                            getCreds()
                            erase()
                    else:
                        with Spinner("Detecting Repository ", tcolors.PURPLE_BOLD):
                            time.sleep(0.3)
                        erase()
                        if subprocess.run(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE).stdout.decode('utf-8').count(':') == 1:
                            getCreds()
                            erase()
                    with Spinner("Versioning/Committing ", tcolors.PURPLE_BOLD):
                        subprocess.check_output(["git", "add", "."])
                        try:
                            subprocess.check_output(["git", "commit", "-m", argv[3]])
                        except:
                            pass
                        time.sleep(0.2)
                    erase()
                    DEVNULL = open(os.devnull, 'w')
                    with Spinner("Pushing Modifications ", tcolors.PURPLE_BOLD):
                        subprocess.check_call(["git", "push", "origin", "master"], stdout=DEVNULL, stderr=subprocess.STDOUT)
                        time.sleep(0.2)
                    DEVNULL.close()
                    erase()
                    print(colorize("Done!", tcolors.GREEN_BOLD))
                except:
                    print(colorize("Sequence exit due to crash. Run again with -t to show the traceback.", tcolors.RED))
                    if "-t" in argv:
                        traceback.print_exc()
            else:
                print(colorize("Error. Please specify a commit message, \n\nExample usage: bit init [origin] ['message']", tcolors.RED))
        else:
            print(colorize("Error. The remote was not a valid.", tcolors.RED))
    else:
        print(colorize("Error. Please specify a remote origin. \n\nExample usage: bit init [origin] ['message']", tcolors.RED))


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
                if subprocess.run(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE).stdout.decode('utf-8').count(':') == 1:
                    getCreds()
                    erase()
                with Spinner("Committing ", tcolors.PURPLE_BOLD):
                    try:
                        subprocess.check_output(["git", "commit", "-m", argv[2]])
                    except:
                        pass
                    time.sleep(0.25)
                erase()
                DEVNULL = open(os.devnull, 'w')
                with Spinner("Pushing Changes ", tcolors.PURPLE_BOLD):
                    subprocess.check_call(["git", "push", "origin", "master"], stdout=DEVNULL, stderr=subprocess.STDOUT)
                    time.sleep(0.25)
                DEVNULL.close()
                erase()
                print(colorize("Done!", tcolors.GREEN_BOLD))
            except Exception:
                print(colorize("Sequence exit due to crash. If you have 2FA enabled, run ") + colorize("bit pass", tcolors.PURPLE_BOLD) + colorize(" and set the password to a Personal Access Token generated from GitHub's website. Run again with -t to show the traceback.", tcolors.RED))
                if "-t" in argv:
                    traceback.print_exc()
        else:
            print(colorize("Error. Please specify a commit message. \n\nExample usage: bit push [message]", tcolors.RED))

    # init repo, then push
    elif argv[1] == "init" or argv[1] == "i":
        if gitFolderExists() == True:
            initRepo(False)
        else:
            initRepo()

    # change password for repository manually
    elif argv[1] == "pass" or argv[1] == "w":
        getCreds()

    # clone repository and cd into it afterwards
    elif argv[1] == "clone" or argv[1] == "c":
        if len(argv) > 2:
            DEVNULL = open(os.devnull, 'w')
            with Spinner("Cloning ", tcolors.BLUE_BOLD):
                subprocess.check_call(["git", "clone", argv[2]], stdout=DEVNULL, stderr=subprocess.STDOUT)
                directory = argv[2].split("/")[-1].split(".")[0]
                # subprocess.check_call(["cd", directory])
                os.chdir(os.getcwd() + "/" + directory)
                time.sleep(0.25)
            DEVNULL.close()
            erase()
            print(colorize("Done!", tcolors.GREEN_BOLD))
        else:
            print(colorize("Error. Please specify a remote. \n\nExample usage: bit clone [remote]", tcolors.RED))       

    # print the help menu
    elif argv[1] == "--help":
        helpMenu()

    else:
        print(colorize("Unknown. Use ", tcolors.RED) + colorize("bit --help", tcolors.RED_BOLD) + colorize(" for correct usage.", tcolors.RED))

# load the encrypted keyfile
def load_key():
    return open(getPath() + "/data/key.key", "rb").read()

if __name__ == "__main__":

    # check if data folder exists, if not, create it
    if not os.path.isdir(getPath() + "/data"):
        with Spinner("First Run - Generating Directories ", tcolors.PURPLE_BOLD):
            os.mkdir(getPath() + "/data")
            time.sleep(0.25)
        erase()

    # check if keyfile exists, if not, create it
    if not os.path.isfile(getPath() + "/data/key.key"):
        key = Fernet.generate_key()
        with Spinner("First Run - Generating Key ", tcolors.PURPLE_BOLD):
            with open(getPath() + "/data/key.key", "wb") as key_file:
                key_file.write(key)
            time.sleep(0.25)
        erase()
       

    # process only if arguments exist in the first place
    if len(argv) > 1:
        processArgs()
    else:
        print(colorize("Error. Use ", tcolors.RED) + colorize("bit --help", tcolors.RED_BOLD) + colorize(" for correct usage.", tcolors.RED))

    # unfreeze terminal, keep workspace changes, EXPERIMENTAL WINDOWS
    if platform.system() == "Linux" or platform.system == "Windows":
        os.system("/bin/bash")
    else:
        os.system("/bin/zsh")