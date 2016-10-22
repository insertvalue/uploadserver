#!/bin/sh

PROGRAM="ibserver"
PID=`ps -ef|grep ibserver|grep -v grep|awk '{print $3}'`

for pid in $PID; do
	kill -9 $pid
done

PID=`ps -ef|grep ibserver|grep -v grep|awk '{print $2}'`

for pid in $PID; do
	kill -9 $pid
done