"""
Reads the HC-SR501 sensor and takes a photo if sensor detects movement.

Sends photo as email to alert email addresses.

"""

from gpio_96boards import GPIO
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import SimpleCV
import socket


def send_email(recipients, subject, message, img_data):
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
        image = MIMEImage(img_data, name='snapshot.png')
        msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, pwd)
        text = msg.as_string()
        server.sendmail(fromaddr, recipients, text)
        server.quit()
    except socket.gaierror:
        print("Network down, can't send email...")

pin = GPIO.gpio_id('GPIO-B')
pins = (
    (pin, 'in')
)
cam = SimpleCV.Camera()
last_detection = False

with GPIO(pins) as gpio:
    while True:
        # If motion detection enabled AND pin is high, take picture and send to alert recipients
        with open('settings.json', 'r') as settingsfile:
            data = json.load(settingsfile)
            if not data['motion_detection']:
                time.sleep(10)
                continue
            else:
                pinValue = gpio.digital_read(pin)
                if pinValue:
                    print ("Motion detected!")
                    img = cam.getImage()
                    img.save("/home/linaro/motion_detection.png")
                    send_email(
                            data['recipients'],
                            "Motion detected!",
                            "Motion was detected, see image attachment!",
                            img)
                    last_detection = True
                else:
                    if last_detection:
                        last_detection = False
                        print ("No motion detected...")
                    time.sleep(10)
