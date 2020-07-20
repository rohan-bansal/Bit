# Bit

_An efficient git-cli alternative with a few power functions to reduce the amount of typing you have to do._


## What is this?

The entire description is in the one-liner above. As of right now, it only has a few functions, but very useful ones!

## Installation

First, clone the repository with:

`git clone https://github.com/Rohan-Bansal/Bit.git`

It's suggested to place the folder in your home directory to keep stuff organized (even though the script will install it globally anyway).

Give the install script run permissions:

`chmod +x ./install.sh`

Install the tool and restart your terminal:

`./install.sh && source ~/.bashrc`

If you use Mac then replace `~/.bashrc` with `~/.zshrc`.


## Usage

__NOTE: Parts of this tool will only work on Windows if a Bash emulator is used.__

The following information and a bit more can be found by running `bit --help` in a terminal.

This project started with the following command (one less to type since it was used so often) that clones the repository and cd's into it afterwards:

`bit clone [remote]`

Initializing a repository, connecting to a remote origin, adding all files in the directory, committing them, then finally pushing can all be done in one command!

`bit init [remote] [message]`

Another repetitive task is committing and pushing changes; To add all files, commit, and push:

`bit push [message]`


It even spices up a bland terminal with some epic colors! 

## To Do

- Progress bar instead of spinning dial
- Optimize
- Utilize encryption
- Support for 2FA
