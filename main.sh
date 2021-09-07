#!/bin/bash

function displayResult(){
    if [ "$?" -eq 0 ]; then
        echo "- - - - - - - - - - - - - - - - - - - -"
        echo "-                                     -"
        echo "-              succssed               -"
        echo "-                                     -"
        echo "- - - - - - - - - - - - - - - - - - - -"  
    else
        echo "- - - - - - - - - - - - - - - - - - - -"
        echo "-                                     -"
        echo "-               failed                -"
        echo "-                                     -"
        echo "- - - - - - - - - - - - - - - - - - - -"
	fi
}		

# Download firmware		
python usb_downloadfirmware.py

# ADC power
python iicadc_ads1115.py

# Config serial
stty -F $(ls /dev/ttyACM*) raw speed 115200
stty -F $(ls /dev/ttyACM*) raw speed 115200
stty -F $(ls /dev/ttyACM*) raw speed 115200

# Clear buffer
echo "" > temporary_log

#gpio
./gpio.sh

# Background buffer
cat $(ls /dev/ttyACM*) >> temporary_log &
buffer_process=$!

#Erase flash
echo "flash erase GD25Q16C 0" > $(ls /dev/ttyACM*)
sleep 0.3
grep -w "Erase success" temporary_log && displayResult || displayResult

#Write flash
echo "flash write GD25Q16C 0 0x1234" > $(ls /dev/ttyACM*)
sleep 0.3
grep -w "OK" temporary_log && displayResult || displayResult

# Read flash
echo "flash read GD25Q16C 0 4" > $(ls /dev/ttyACM*)
sleep 0.1
grep -w "34 12 00 00" temporary_log && displayResult || displayResult


kill -9 "$buffer_process"  # The data format of IIC cannot be displayed normally in the temporary log.

# Read iic address
echo "i2c scan I2C_0" > $(ls /dev/ttyACM*)
sleep 0.1
cat $(ls /dev/ttyACM*)



