#!/bin/bash

declare -a arr=("version" "auth" "list" "post" "list" "clear" "list")

cmd=./trmeet.py
flags="-v"

for i in "${arr[@]}"
do
    echo `$cmd $flags $i`
    echo "---------------------"
done


