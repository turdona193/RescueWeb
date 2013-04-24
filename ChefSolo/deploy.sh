#!/bin/bash
# This is the deployment script, run on the development host
# Script cribbed from 
# http://www.opinionatedprogrammer.com/2011/06/chef-solo-tutorial-managing-a-single-server-with-chef/

# Usage: ./deploy.sh [host]
#        if host is omitted, defaults to the host named in next line

host="${1:-ubuntu@ec2-54-225-207-196.compute-1.amazonaws.com}"
ssh-add ~/.ssh/teamMurrica.pem



# The host key might change when we instantiate a new VM, so
# we remove (-R) the old host key from known_hosts
ssh-keygen -R "${host#*@}" 2> /dev/null

# everything after the last ' on the next line down to the final '
# executes on host
cd chef && tar cj . | ssh -o 'StrictHostKeyChecking no' "$host" '
sudo rm -rf ~/chef &&
mkdir ~/chef &&
cd ~/chef &&
tar xj &&
sudo bash install.sh'
