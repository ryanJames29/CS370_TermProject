import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522


USER_UID = 596170611542
reader = SimpleMFRC522()

try:
        for i in range(5):
                print("Waiting")
                id = reader.read_id()
                print("the ID is",id)
                #print("UID (Hex):", format(id, '02x'))
                if (id == USER_UID):
                        print("User approved")
                else:
                        print("Rejected")
                time.sleep(4)
finally:
        GPIO.cleanup()