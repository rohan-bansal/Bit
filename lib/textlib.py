from lib.tcolors import tcolors
from random import choice

phrases = [
    "purged the optronic neogenic emergency rocket",
    "decluttered the microfilament bio-tubing",
    "destabiled the graviton energy core",
    "inverted the nuclear delta-wave landing brackets",
    "replaced the optronic polar flipper",
    "installed the ionic bipolar replicator",
    "restarted the dorsal stabilizer",
    "diverted power from the magnesium driver",
    "calibrated the rubidium defragmentor",
    "scrubbed interdimensional portal bracket",
    "ejected caesium landing cushion",
    "realigned the side electro-ceramic thrusters",
    "nerfed power to the quantum propeller",
    "boosted bionic teleporter pads"
]

# a small function to colorize text
def colorize(text, color):
    return color + text + tcolors.RESET

def getRandomPhrase():
    return choice(phrases)