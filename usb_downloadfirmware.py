#!/usr/bin/python

import subprocess
import datetime
import os
import time
import shlex
import serial
from serial.tools import list_ports
from time import sleep
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


#USB download msp430 firmware
if timeout_command(msp430_command, 10) == 0:
    #print (time.strftime(" %H:%M:%S ", time.localtime()) + "!!!!DEBUG!!!!" + str(Comunicate)) 
    if "OK" in str(Comunicate):
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download msp430 firmware completed")
        displayResult(True)
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "< The board need to power on again. >")
    else:
        #print (time.strftime(" %H:%M:%S ", time.localtime()) + " ! DEBUG ! ")
        print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download msp430 firmware failed")
        displayResult(False)
else:
    print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download msp430 firmware failed")
    displayResult(False)

sleep(10)   #The board is powered on again.

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


#Flash test
# if timeout_command("cat $(ls /dev/ttyACM*)", 50) == 0:
    # print (time.strftime(" %H:%M:%S ", time.localtime()) + str(Comunicate)) 
# else:
    # print (time.strftime(" %H:%M:%S ", time.localtime()) + "USB download cc1352 firmware failed")
    # displayResult(False)  
    
