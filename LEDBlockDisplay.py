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
                led.printLetter(string[i], False, 1)
                time.sleep(LED_SCROLL_PAUSE)
    finally:
        led.clearDisplays()
        led.cleanup()

def led_print_numbers(numbers):
    numbers = str(numbers)
    try:
        for i in range(0, len(numbers)):
            led.printNumber(numbers[i], False, 1)
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
        numOfDevices = 2
        led = LEDBlock(gpio, numOfDevices, 'GPIO-E', 'GPIO-D', 'GPIO-C')
        while 1 is 1:
            with open('sensordata.json', 'r') as datafile:
                sensordata = json.load(datafile)
                print(str(sensordata['t']) + ' ' + str(sensordata['h']))
                led.printLetter('T', False, 2)
                led.printLetter('T', False, 1)
                time.sleep(1)
                print_arr = str(round(sensordata['t'])).split('.')
                led.printNumber(print_arr[0][0], 1)
                led.printNumber(print_arr[0][1], 2)
                time.sleep(1)
                # for i in print_arr[0]:
                #     led.printNumber(i, 1)
                #     time.sleep(1)
                # led.printDice(1, 1)
                # time.sleep(1)
                # for i in print_arr[1]:
                #     led.printNumber(i, 1)
                #     time.sleep(1)
                led.printLetter('H', False, 2)
                led.printLetter('H', False, 1)
                time.sleep(1)
                print_arr = str(round(sensordata['h'])).split('.')
                led.printNumber(print_arr[0][0], 1)
                led.printNumber(print_arr[0][1], 2)
                time.sleep(1)
                # for i in print_arr[0]:
                #     led.printNumber(i, 1)
                #     time.sleep(1)
                # led.printDice(1, 1)
                # time.sleep(1)
                # for i in print_arr[1]:
                #     led.printNumber(i, 1)
                #     time.sleep(1)

