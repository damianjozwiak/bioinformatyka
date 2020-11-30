#!/bin/bash

for file in input/*
do
	if [[ $file != *.seq ]]
	then
		python3 sbh.py $file
		# printf '\n'
	fi
done
