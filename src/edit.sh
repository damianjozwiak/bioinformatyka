#!/bin/bash


for f in *.seq
do
	head -c10 $f | cat - ${f%.*} > temp;
	sed -i 's/600/\n600/' temp;
	mv temp ${f%.*}
done

