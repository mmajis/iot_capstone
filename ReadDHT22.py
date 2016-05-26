"""
Reads the DHT22 sensor and stores in a file.

Sends alert emails if thresholds are crossed.

"""

import Adafruit_DHT
import datetime
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket



def send_email(recipients, subject, message):
    try:
        pwd = None
        with open('secrets.json', 'r') as secretsfile:
            secrets = json.load(secretsfile)
            pwd = secrets['smtp_pwd']

        fromaddr = "mmajis@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, pwd)
        text = msg.as_string()
        server.sendmail(fromaddr, recipients, text)
        server.quit()
    except socket.gaierror:
        print("Network down, can't send email...")

while True:

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
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

#humidity = 50
#temperature = 40

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        with open('sensordata.json', 'w') as datafile:
            datafile.write('{"t": %.1f, "h": %.1f, "time": "%s"}' % (temperature, humidity, datetime.datetime.now().isoformat()))
        with open('settings.json', 'r') as settingsfile:
            settings = json.load(settingsfile)
            message = ""
            if temperature > settings['temperature_threshold']:
                message += "Temperature %d exceeds threshold %d\n\n" % (temperature, settings['temperature_threshold'])
            if humidity > settings['humidity_threshold']:
                message += "Humidity %d exceeds threshold %d\n\n" % (humidity, settings['humidity_threshold'])
            if message is not None:
                send_email(settings['recipients'], "Sensor alert!", message)

    else:
        print('Failed to get reading. Try again!')
    time.sleep(5)

