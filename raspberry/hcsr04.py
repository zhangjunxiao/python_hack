import RPi.GPIO as GPIO
import datetime
import time


GPIO.cleanup()

Trig_Pin = 20
Echo_Pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)

time.sleep(2)

file_name = "a.text"
# path = "/home/zjx/www"
def checkdist():

    file = open(file_name, 'a')

    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    distance = (t2-t1)*340*100/2
    dateStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(dateStr + " distance: [" +str(distance)+"]" + "\n")
    return (t2-t1)*340*100/2

try:
    while True:
        print 'Distance:%0.2f cm' % checkdist()
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
