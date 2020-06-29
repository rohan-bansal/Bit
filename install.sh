#!/bin/bash

# CHMOD +X THIS FILE

loc=$(pwd)/bit.py

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "alias bit='python3 $loc'" >> ~/.bashrc
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "alias bit='python3 $loc'" >> ~/.zshrc
elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "alias bit='python3 $loc'" >> ~/.bashrc
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "alias bit='python3 $loc'" >> ~/.bashrc
elif [[ "$OSTYPE" == "win32" ]]; then
    echo "alias bit='python3 $loc'" >> ~/.bashrc
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    echo "alias bit='python3 $loc'" >> ~/.bashrc
else
    echo "Script error."
fi