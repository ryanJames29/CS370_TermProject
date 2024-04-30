from gpiozero import RGBLED
import time

led = RGBLED(22,27,17)
def setLight(numUsers):
        if(numUsers == 0):
                led.color = (1,0,0)
                time.sleep(0.5)
        elif(numUsers ==  1):
                led.color = (0,1,0)
                time.sleep(0.5)
                led.off()
                time.sleep(0.25)
        else:
                led.color = (0,1,1)
                time.sleep(0.5)
                led.off()
                time.sleep(0.25)


users = [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1]

for i in users:
        setLight(i)