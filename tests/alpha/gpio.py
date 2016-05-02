from bbio import *
import time

tp = GPIO1_16
pinMode(tp, OUTPUT)
while 1:
    digitalWrite(tp, HIGH)
    print digitalRead(tp)
    time.sleep(1)
    digitalWrite(tp, LOW)
    print digitalRead(tp)
