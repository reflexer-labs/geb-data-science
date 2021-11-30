#!/bin/bash
sed 's/(Eastern Daylight Time)//g' < $1  > $1.tmp
mv $1.tmp $1
