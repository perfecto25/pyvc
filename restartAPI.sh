#!/bin/sh
lastpid=$(ps -ef | grep pyvc_api.py | grep -v grep | awk -F" " {'print $2'})

kill -9 $lastpid

python pyvc_api.py &
