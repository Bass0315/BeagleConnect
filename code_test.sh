
sta=true

for (( i = 0; i < 100; i++ )); do 
	if [ "$sta" -ep 0 ]; then
		echo "i2c write I2C_0 0x48 0x01" > $(ls /dev/ttyACM*)
	else
		echo "i2c write I2C_0 0x48 0x00" > $(ls /dev/ttyACM*)
	fi
	sta=!sta	
done	
