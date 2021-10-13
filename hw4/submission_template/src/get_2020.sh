#!/bin/bash

# trim to only needed columns and get 2020 SRs

#awk -F',' '$3 ~ /2020/ {print $1","$2","$3","$9}' $1 > data/awk_results.txt

# handles commas inside of double quotes
awk -v FPAT='([^,]*)|("[^"]*")' '$3 ~ /2020/ {print $1","$2","$3","$9}' $1 > data/awk_results.txt
