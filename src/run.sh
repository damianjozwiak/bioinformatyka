#!/bin/bash

for file in input/*
do
	if [[ $file != *.seq ]]
	then
		python3 sbh.py $file
	fi
done
