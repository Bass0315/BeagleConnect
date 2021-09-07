"""
https://github.com/adafruit/Adafruit_Python_ADS1x15
"""

import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
GAIN = 4

re_sat = False

print(' ADC ADS1x15 values ')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)

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
        
# Main loop.
for i in range(5):
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        for j in range(10):
            values[i] += adc.read_adc(i, gain=GAIN) 
      
        values[i] = (values[i] / 10 * 2 - 2000)/10000.0
        
        #print (time.strftime(" %H:%M:%S ", time.localtime()) + "!!!!DEBUG!!!!" + str(i == 0 and 3.3-3.3*0.05 < values[i] and values[i] < 3.3+3.3*0.05))
        if i == 1 :
            if 3.3-3.3*0.05 < values[i] and values[i] < 3.3+3.3*0.05 :
                re_sat = True
            else:
                re_sat = False
        if i == 0 :
            if 5-5*0.05 < values[i] and values[i] < 5+5*0.05 :
                re_sat = True
            else:
                re_sat = False
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.1)

displayResult(re_sat)