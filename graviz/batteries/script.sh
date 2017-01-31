#!/bin/bash
for i in $(seq 0 100); do
	convert "stat_sys_battery_$i.png" -strip -rotate 90 -unsharp 0x30 -resize 200x200 -unsharp 0x5 -gravity center -pointsize 40 -stroke "#000C" -strokewidth 2 -annotate 0 "$i%" -stroke none -fill white -annotate 0 "$i%" -quality 100 -set units PixelsPerInch -density 300 "./battery_$i.png"
done
