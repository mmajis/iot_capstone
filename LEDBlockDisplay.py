#!/usr/bin/python
import time
from LED.LEDProcessor import LEDBlock
import Adafruit_DHT

LED_SCROLL_PAUSE = 0.2

def led_print(text):
    string = text.upper()
    try:
        for i in range(0, len(string)):
            if i == 0:
                led.printLetter(' ', True, 1)
                led.printLetter(string[i], True, 2)
                time.sleep(LED_SCROLL_PAUSE)
            elif i == len(string) - 1:
                led.printLetter(string[i], True, 1)
                led.printLetter(' ', True, 2)
                time.sleep(LED_SCROLL_PAUSE)
            else:
                led.printLetter(string[i], True, 1)
                led.printLetter(string[i + 1], True, 2)
                time.sleep(LED_SCROLL_PAUSE)
        led.printLetter(' ', True, 1)
    finally:
        led.clearDisplays()
        led.cleanup()


if __name__ == '__main__':
    numOfDevices = 2
    led = LEDBlock(numOfDevices)

    # Sensor should be set to Adafruit_DHT.DHT11,
    # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
    sensor = Adafruit_DHT.DHT22

    # Example using a Beaglebone Black with DHT sensor
    # connected to pin P8_11.
    # pin = 'P8_11'

    # Example using a Raspberry Pi with DHT sensor
    # connected to GPIO23.
    pin = 23

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    led_print ('h %s t %s' % (1, 2))

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    #if humidity is not None and temperature is not None:
    #    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    #    led_print('T %s H %s' % (temperature, humidity))
    #else:
    #    print('Failed to get reading. Try again!')
