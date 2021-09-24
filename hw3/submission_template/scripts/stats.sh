#!/bin/bash

# checks for at least 10000 lines
if [[ $(wc -l < $1) -lt 10000 ]]
then
    echo Error: the input file must have at least 10,000 lines
    exit 1
fi

# printing stats
wc -l < $1
head -n 1 $1
tail -n 10000 $1 | grep -i "potus" | wc -l
sed -n '100,200p' $1 | grep "fake" | wc -l