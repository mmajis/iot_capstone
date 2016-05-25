#!/usr/bin/python
import time
from LED.LEDProcessor import LEDBlock
import json
from gpio_96boards import GPIO

LED_SCROLL_PAUSE = 0.5

def led_print_text(text):
    string = text.upper()
    try:
        for i in range(0, len(string)):
                led.printLetter(string[i], True, 1)
                time.sleep(LED_SCROLL_PAUSE)
    finally:
        led.clearDisplays()
        led.cleanup()

def led_print_numbers(numbers):
    numbers = str(numbers)
    try:
        for i in range(0, len(numbers)):
            led.printNumber(numbers[i], True, 1)
            time.sleep(LED_SCROLL_PAUSE)
    finally:
        led.clearDisplays()
        led.cleanup()


if __name__ == '__main__':
    global DIN
    global CS
    global CLK
    DIN = GPIO.gpio_id('GPIO-E')
    CS = GPIO.gpio_id('GPIO-D')
    CLK = GPIO.gpio_id('GPIO-C')
    global pins
    print DIN
    pins = (
        (DIN, 'out'),
        (CS, 'out'),
        (CLK, 'out')
    )

    with GPIO(pins) as gpio:
        numOfDevices = 1
        led = LEDBlock(gpio, numOfDevices, 'GPIO-E', 'GPIO-D', 'GPIO-C')
        while 1 is 1:
            with open('sensordata.json', 'r') as datafile:
                sensordata = json.load(datafile)
                led.printLetter('T')
                time.sleep(1)
                led.printNumber(sensordata['t'])
                time.sleep(1)
                led.printLetter('H')
                time.sleep(1)
                led.printNumber(sensordata['h'])

