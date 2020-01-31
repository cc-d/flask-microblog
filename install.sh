#!/usr/bin/sh
# Only intended to run on a headless debian 10 server,
# it should be fairly easy to change this script to do what
# you need it to do if on a different distro or OS.

# Need to run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi 

apt-get update
apt-get upgrade
apt-get install python3-pip postgresql sqlite3
pip3 install -r requirements.txt

service postgresql restart

su - postgres -c "createdb microblog"
su - postgres -c "psql microblog -c \"DROP SCHEMA public CASCADE;\""
su - postgres -c "psql microblog -c \"CREATE SCHEMA public;\""
su - postgres -c "psql microblog -c \"GRANT ALL ON SCHEMA public TO postgres;\""
su - postgres -c "psql microblog -c \"GRANT ALL ON SCHEMA public TO public;\""
su - postgres -c "psql microblog -c \"COMMENT ON SCHEMA public IS 'standard public schema';\""
su - postgres -c "psql microblog -c \"CREATE USER test WITH PASSWORD 'test';\""
su - postgres -c "psql microblog -c \"ALTER SCHEMA public OWNER to postgres;\""

echo "installed microblog"