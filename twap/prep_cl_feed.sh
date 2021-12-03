#!/bin/bash
sed 's/ (Eastern Daylight Time)//g' < $1  > $1.tmp
sed 's/ (Eastern Standard Time)//g' < $1.tmp  > $1.tmp2
rm $1.tmp
mv $1.tmp2 $1
