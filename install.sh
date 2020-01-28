#!/usr/bin/sh
# Only intended to run on a headless debian 10 server,
# it should be fairly easy to change this script to do what
# you need it to do if on a different distro or OS.

# Ned to run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi 

apt-get update
apt-get upgrade
apt-get install python3-pip postgresql sqlite3
pip3 install -r requirements.txt

sudo -u postgres createuser --superuser microblog_user
sudo -u microblog createdb microblog