#!/bin/sh

ibserver_file="ibserver.tar.gz"
ibserver_runtime_file="ibserver_runtime.debug"

if [ -f "$ibserver_file" ]; then
	tar zxf $ibserver_file
	rm -rf $ibserver_file
fi

if [ ! -f "$ibserver_runtime_file" ]; then
	touch "$ibserver_runtime_file"
fi

cd ibserver
PROGRAM="ibserver"

PRO_NOW=`ps aux | grep $PROGRAM | grep -v grep | wc -l`

if [ $PRO_NOW -gt 0 ] ; then
	killall -9 $PROGRAM
fi

PRO_STAT=`ps aux|grep $PROGRAM |grep T|grep -v grep|wc -l`

if [ $PRO_STAT -gt 0 ] ; then
	killall -9 $PROGRAM
	sleep 2
	date "+%Y-%m-%d %H:%M:%S">>../"$ibserver_runtime_file"
	echo "start unzip...">>../"$ibserver_runtime_file"
	echo>>../"$ibserver_runtime_file"
	python ibserver.py>/dev/null 1>&2 &
fi

while true ; do

    PRO_NOW=`ps aux | grep $PROGRAM | grep -v grep | wc -l`

    if [ $PRO_NOW -lt 1 ] ; then
		date "+%Y-%m-%d %H:%M:%S">>../"$ibserver_runtime_file"
		echo "start unzip...">>../"$ibserver_runtime_file"
		echo>>../"$ibserver_runtime_file"
        python ibserver.py>/dev/null 1>&2 &
    fi

    PRO_STAT=`ps aux|grep $PROGRAM |grep T|grep -v grep|wc -l`

    if [ $PRO_STAT -gt 0 ] ; then
        killall -9 $PROGRAM
        sleep 2
		date "+%Y-%m-%d %H:%M:%S">>../"$ibserver_runtime_file"
		echo "start ibserver...">>../"$ibserver_runtime_file"
		echo>>../"$ibserver_runtime_file"
        python ibserver.py>/dev/null 1>&2 &
    fi
    sleep 5

done

exit 0