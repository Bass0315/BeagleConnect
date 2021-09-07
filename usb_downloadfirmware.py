import subprocess
import datetime
import os
import time
import shlex
import serial
from serial.tools import list_ports
from time import sleep
# import RPi.GPIO as GPIO
import pigpio
#from FileControl import fileOperate

msp430_command = r"sudo python2 -m msp430.bsl5.hid -e -P  usb_uart_bridge.hex"
cc1352_command = r"python3 cc2538-bsl.py zephyr.bin $(ls /dev/ttyACM*)"
 
#Download wifi program
def timeout_command(command, timeout):
    """
    call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None
    """
    # if type(command) == type(''):          # Adding these two sentences will cause an error.
        # command = shlex.split(command)
    global Comunicate
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    resultcode = process.poll()
    while resultcode is None:
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:  
            process.kill()
            return -1
        sleep(0.01)
        resultcode = process.poll()
    Comunicate = process.communicate()    
    return resultcode
    
    
def displayResult(flag):
    if flag == True:
        print ("- - - - - - - - - - - - - - - - - - - -")
        print ("-                                     -")
        print ("-              succssed               -")
        print ("-                                     -")
        print ("- - - - - - - - - - - - - - - - - - - -")  
    else:
        print ("- - - - - - - - - - - - - - - - - - - -")
        print ("-                                     -")
        print ("-               failed                -")
        print ("-                                     -")
        print ("- - - - - - - - - - - - - - - - - - - -") 


timeout_command("sudo pigpiod", 10)
print (time.strftime(" %H:%M:%S ", time.localtime()) + "< Please press the Boot button. >")
pigpio.pi().write(4,1)
sleep(5)
pigpio.pi().write(4,0)
print (time.strftime(" %H:%M:%S ", time.localtime()) + "< Please release the Boot button. >")
sleep(5)


#USB download msp430 firmware
if timeout_command(msp430_command, 10) == 0:
    #print (time.strftime(" %H:%M:%S ", time.localtime()) + "!!!!DEBUG!!!!" + str(Comunicate)) 
    if "OK" in str(Comunicate):
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download msp430 firmware completed")
        displayResult(True)
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "< The board is powering up again. >")
    else:
        #print (time.strftime(" %H:%M:%S ", time.localtime()) + " ! DEBUG ! ")
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download msp430 firmware failed")
        displayResult(False)
else:
    print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download msp430 firmware failed")
    displayResult(False)

pigpio.pi().write(4,1)
sleep(2)   #The board is powered on again.
pigpio.pi().write(4,0)
sleep(2)   #The board is powered on again.


#USB download cc1352 firmware
if timeout_command(cc1352_command, 50) == 0:
    #print (time.strftime(" %H:%M:%S ", time.localtime()) + "!!!!DEBUG!!!!" + str(Comunicate)) 
    if "Write done" in str(Comunicate):
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download cc1352 firmware completed")
        displayResult(True)
    else:
        #print (time.strftime(" %H:%M:%S ", time.localtime()) + " ! DEBUG ! ")
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download cc1352 firmware failed")
        displayResult(False)
else:
    print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download cc1352 firmware failed")
    displayResult(False)   

    
