#!/bin/bash

# remove lines with missing zip

awk -F',' '{if ($4 != "" && $4 != "N/A") print $0}' $1 > data/awk_clean.csv