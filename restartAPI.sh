#!/bin/sh 

api='pyvc_api.py'

lastpid=$(ps -ef | grep $api | grep -v grep | awk -F" " {'print $2'})

if [[ $lastpid ]]
then
    pkill -f $api
fi

echo "restarting $api.."
python $api &

if [ $? == 0 ]
then
    echo "done"
else
    echo "errors starting $api"
fi