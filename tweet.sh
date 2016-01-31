#!/bin/bash

while true
 do
  waittime=$[($RANDOM % 300) + 1]
  #sleep $[$waittime]m
  date >> tweets.log
  #python helloworld.py  >> tweets.log
  /home/ubuntu/miniconda/bin/python tweet.py >> tweets.log
  echo wait: $waittime min  >> tweets.log
  echo "------------------------------------------------------------" >> tweets.log
  sleep $[$waittime]m
 done

