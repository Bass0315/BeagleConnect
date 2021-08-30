#!/bin/bash

chip_gpio=("23" "6" "28" "17" "16" "24" "5" "27" "19" "20")

# config and int gpio	
for i in $(seq 0 $((${#chip_gpio[*]}-1))) 
do
	command="gpio conf GPIO_0 ${chip_gpio[$i]} out"
	echo ${command} > $(ls /dev/ttyACM*)
	command="gpio set GPIO_0 ${chip_gpio[$i]} 1"
	echo ${command} > $(ls /dev/ttyACM*)
done

sleep 2

# reset gpio
for i in $(seq 0 $((${#chip_gpio[*]}-1))) 
do
	command="gpio set GPIO_0 ${chip_gpio[$i]} 0"
	echo ${command} > $(ls /dev/ttyACM*)
done
