#!/bin/bash

for i in {00..09}; do
  filename="data/cities_${i}.csv"
  echo -e "\nSimulating On $filename"
  python AS.py -f "$filename" --saveplot "data/cities_${i}.png"
done
