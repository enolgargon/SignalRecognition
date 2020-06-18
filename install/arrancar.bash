#!/bin/bash

function check_and_run {
	run=$(ps -ef | grep -v grep | grep $1 | wc -l)

	if (($run > 0))
	then
		return
	else
		cd /home/recognition/SignalRecognition
		source venv/bin/activate
		python3 -m $1 &
	fi
}

check_and_run screen_control
check_and_run logic
check_and_run camera_control

run=$(ps -ef | grep -v grep | grep "firefox" | wc -l)
if (($run > 0))
then
	exit
else
	firefox file:///home/recognition/SignalRecognition/gui/gui.html &
fi
