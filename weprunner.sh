#!/bin/sh
echo "ARG: $1"
cd wepapp
python wep.py ../$1
