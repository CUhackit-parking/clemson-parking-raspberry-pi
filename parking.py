import json
import RPi.GPIO as GPIO
import time
from time import sleep
import grove_display
import time, threading
import requests

url = "https://getpantry.cloud/apiv1/pantry/b3e96063-a141-4c97-8deb-ca7ae6b8fe83/basket/parking1"
header = {"Content-Type": "application/json"}

increment_url = "https://api.clemsonparking.tech/lot/C-16/increment/{}"
decrement_url = "https://api.clemsonparking.tech/lot/C-16/decrement"

get_item = "https://api.clemsonparking.tech/lot/C-16"
def periodic_sync():
    sync()
    threading.Timer(60,periodic_sync).start()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

changing_cars = 0

cars = 0

count = 0

readings = {"Count" : 0, "LotSize":20}


def sync():
    global changing_cars
    global cars
    try:
        
        print(changing_cars)
        
        
        
        response = requests.patch(increment_url.format(changing_cars))
        if response.status_code ==  200:
            changing_cars = 0
        
        response = requests.get(get_item).json()
        cars = response["count"]
        print(cars)
        print(changing_cars)
        print()
        
    except Exception as e:
        print(e)
        



debounce = False
while(True):
    if (GPIO.input(12) == GPIO.HIGH or  GPIO.input(8) == GPIO.HIGH) and(not debounce):
        #write code to set count to current count based of api
        if GPIO.input(8) == GPIO.HIGH:
            changing_cars += 1
        elif cars + changing_cars > 0:
            changing_cars -= 1
            
      
      
       
        debounce = True
        time.sleep(.02)
        sync()
        
        
        lot_remain = requests.get(get_item).json()
        
        lot_remain = lot_remain["capacity"]
        
        
        
        
        
        
        
        
        
        spots_remaining = lot_remain - cars - changing_cars
        
        if spots_remaining <= 0:
            grove_display.setText("FULL")
            grove_display.setRGB(255,0,0)
        else:
            if(spots_remaining) < 15 and spots_remaining >0:
                grove_display.setRGB(255,255,0)
            else:
                grove_display.setRGB(0,255,0)
            grove_display.setText("Spots remaining: {}".format(spots_remaining))
        
        
        
    else:
        debounce = False
        
    



print(lot_number)
print(readings)


