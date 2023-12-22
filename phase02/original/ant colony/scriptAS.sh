#!/bin/bash

for i in {000..002}; do
  filename="data/points3D_${i}.csv"
  echo -e "\nSimulating On $filename"
  python AS.py -f "$filename" --saveplot "data/path3D_${i}_as.png" --iterationplot "data/path3Dlength_${i}_as.png"
done
