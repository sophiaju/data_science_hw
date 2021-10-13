#!/bin/bash

# remove lines with missing zip

awk -F',' '$4 != ""' $1 > data/awk_clean.csv