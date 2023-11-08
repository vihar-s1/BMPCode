#!/bin/bash

for i in {00..09}; do
  filename="data/points_${i}.csv"
  echo -e "\nSimulating On $filename"
  python AS.py -f "$filename" --saveplot "data/path_${i}_as.png" --iterationplot "data/pathlength_${i}_as.png"
done
