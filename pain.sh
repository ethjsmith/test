#!/bin/bash

# this section checks if you're running as root
if [ "$EUID" -ne 0 ]
  then echo "please run as root"
  exit
fi
# now the fun begins
shutdown -now
