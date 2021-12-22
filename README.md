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





