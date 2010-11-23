#! /usr/bin/env python
 
from os import fork, chdir, setsid, umask, listdir
from random import choice
from sys import exit
from time import sleep
from datetime import datetime
import subprocess

RECORDING_DIR='/var/lib/mythtv/recordings_pretty'
LOG_FILE='/mnt/tv/log/transcode_daemon.log'
TRANSCODE_SCRIPT='/mnt/tv/scripts/transcode'

def log(msg):
   open(LOG_FILE, "a").write("[" + str(datetime.now()) + "]: DAEMON " + msg + "\n");
 
def main():
  while 1:
    sleep(5)
    # get a random file from the recordings dir
    flist = listdir(RECORDING_DIR)
    if len(flist) > 0:
      transcode_file = choice(flist)
      log(transcode_file)
      subprocess.call([TRANSCODE_SCRIPT, transcode_file])
 
# Dual fork hack to make process run as a daemon
if __name__ == "__main__":
  try:
    pid = fork()
    if pid > 0:
      exit(0)
  except OSError, e:
    exit(1)
 
  chdir("/")
  setsid()
  umask(0)
 
  try:
    pid = fork()
    if pid > 0:
      exit(0)
  except OSError, e:
    exit(1)
 
  main()
