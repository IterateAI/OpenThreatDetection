#!/bin/sh
echo "ARG: $1"
cd wepapp
python3 wep.py ../$1
