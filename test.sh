#!/bin/bash

declare -a arr=("version" "auth" "list" "post" "list" "clear" "list")

bin=trmeet.py
flags="-v"

for i in "${arr[@]}"
do
    cmd="./$bin $flags $i"
    echo $cmd
    echo "---------------------"
    echo `$cmd`
    echo "---------------------"
done


