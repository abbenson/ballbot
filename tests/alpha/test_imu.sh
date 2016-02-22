#!/bin/bash
echo Initializing Serial
python ./test_imu.py
echo Connecting to IMU
minicom -b 57600 -D /dev/ttyO1