# bit 2.0

Do you insist on using terminal git instead of Github Desktop? Do you also secretly wish you had to type less? `bit` is the solution :sunglasses:

### Installation

**Linux, Mac, Windows (WSL)**

The included script will alias bit in the `bashrc` file. Modify the script for different shells if needed.

1. Clone the repository
2. Give the install script permissions:`chmod +x install.sh`
3. Run the install script: `./install.sh`

**DIY**

1. Clone the repository
2. alias the `bit` keyword to `python3 <location of clonedRepo/bit.py file>`





### Usage

*All of the following descriptions are also available @ `bit --help`*



**`bit create`**

Will initialize a new repository in the current directory. 

**`bit create -m <msg>`**

Will initialize a new repository in the current directory, and run `git add .` and `git commit -m <msg>`

<br/>

**`bit commit`**

Will run `git add .` and `git commit -m <msg>` where msg is prompted (press enter for technobabble :P)

**`bit commit -m <msg>`**

Will run `git add .` and `git commit -m <msg>`

<br/>

**`bit push`**

Will push local to remote using `git push origin <branch>` (error on conflicts)

**`bit push -c`**

Will run `bit commit` to add/commit all files, then push

**`bit push -f`**

Will force push changes (with a confirmation prompt)

<br/>

**`bit origin`**

Will return the currently configured remote URL (error if does not exist)

**`bit origin -s <url>`**

Will add the remote URL if it does not exist, and change it if it does

<br/>

**`bit pull`**

Will pull changes from current branch (error if merge conflict)

<br/>

**`bit fetchall`**

Will fetch all remote changes with `git fetch --all`

<br/>

**`bit newrepo`**

Will launch a browser tab to create a new repo on GitHub

<br/>

**`bit checkout <branch>`**

Will create a branch if it does not exist, or switch to it if it does
