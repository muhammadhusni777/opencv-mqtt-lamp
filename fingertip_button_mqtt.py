#interpreter C:/Users/User/AppData/Local/Programs/Python/Python38/python.exe

import context
import paho.mqtt.client as mqtt
import calendar 
import time 
import datetime
import sched

import cv2
#import pyfirmata
from cvzone.HandTrackingModule import HandDetector
from cvzone.FPS import FPS

cap = cv2.VideoCapture(0)
#Set size screen
x_max, y_max = 1280, 720
cap.set(3, x_max)
cap.set(4, y_max)



def on_connect(mqttc, obj, flags, rc):
    #print("rc: " + str(rc))
    
    print(" ")

def on_message(mqttc, obj, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload)
    #print(datetime.datetime.now())
    
    a = str(msg.payload.decode("UTF-8"))
    
    #print('This message will be written to a file.', file=f)
    #month = datetime.datatime.now()    
    '''
    filename = "ho1.txt" 
    
    print(datetime.datetime.now(), end = " ")
    
    print(a)
    
    fh = open(filename, 'a')
    fh.write(str(datetime.datetime.now()))
    fh.write(str(a))
    fh.write("\n")
    
    print("")
    print(datetime.datetime.now(), end = " ")
    
    
    
    print(a)
    
    fh.write(str(datetime.datetime.now()))
    fh.write(str(a))
    fh.write("\n")

    fh.close()
    mqttc.publish("reset", "off",1)
    #print(msg.payload.replace('b',''))
    '''
    
    
    
def on_publish(mqttc, obj, mid):
    #print("mid: " + str(mid))
    print()
    

def on_subscribe(mqttc, obj, mid, granted_qos):
    #print("Subscribed: " + str(mid) + " " + str(granted_qos))
    print(" ")
    

def on_log(mqttc, obj, level, string):
    #print(string)
    print (" ")



mqttc = mqtt.Client()
mqttc.publish("reset", "off",1)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("192.168.43.173", 1883, 60)
#mqttc.connect("127.0.0.1", 1883, 60)
#mqttc.subscribe("alldata", 0)

#mqttc.loop_forever()
mqttc.loop_start()




if not cap.isOpened():
    print("Camera couldn't Access")
    exit()

fpsReader = FPS()
fps = fpsReader.update()

detector  = HandDetector(detectionCon=0.7)
#pinR, pinY, pinG = 4, 3, 2
#port = 'COM7' #Select your COM
#board = pyfirmata.Arduino(port)

counter_R, counter_Y, counter_G = 0, 0, 0
R_on, Y_on, G_on = False, False, False

G_val = 0
while True:
    success, img = cap.read()
    #hands, img = detector.findHands(img)
    img = detector.findHands(img)
    fps,img = fpsReader.update(img)
    #fps = fpsReader.update()
    #hands, img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    
    cv2.putText(img, str("put your finger here"), (100, 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        
    if lmList :
        x, y = 100, 100
        w, h = 225, 225
        X, Y = 140, 190

        fx, fy = lmList[8][0], lmList[8][1] #index fingertip
        posFinger = [fx, fy]
        cv2.circle(img, (fx, fy), 15, (255, 0, 255), cv2.FILLED) #draw circle on index fingertip
        cv2.putText(img, str(posFinger), (fx+10, fy-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        
        #cv2.putText(img, str("xixixi"), (10, 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        
        # cv2.line(img, (fx-x_max, fy), (fx+x_max, fy), (255,255,0), 2) # x line
        # cv2.line(img, (fx, fy+y_max), (fx, fy-y_max), (255, 255, 0), 2)# y line


        if x < fx < x + w - 95 and y < fy < y + h - 95:
            counter_R += 1
            cv2.rectangle(img, (x, y), (w, h), (255, 255, 0), cv2.FILLED)
            if counter_R == 1:
                R_on = not R_on
        else :
            counter_R = 0
            if R_on:
                R_val = 1
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "on", (X, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
                mqttc.publish("esp32/output", "on")
            else:
                R_val = 0
                cv2.rectangle(img, (x, y), (w, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "off", (X, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 0, 255), 5)
                mqttc.publish("esp32/output", "off")
    cv2.imshow("Image", img)
    cv2.waitKey(1)
'''
        if x + 250 < fx < x + 155 + w and y < fy < y + h - 95: #155 = 250 - 95
            counter_Y += 1
    #        cv2.rectangle(img, (x + 250, y), (w + 250, h), (255, 255, 0), cv2.FILLED)
            if counter_Y == 1:
                Y_on = not Y_on
        else:
            counter_Y = 0
            if Y_on:
                Y_val = 1
      #          cv2.rectangle(img, (x+250, y), (w+250, h), (0, 255, 255), cv2.FILLED)
      #          cv2.putText(img, "on", (X+250, Y), cv2.FONT_HERSHEY_PLAIN,
    #                     5, (255, 255, 255), 5)
            else:
                Y_val = 0
     #           cv2.rectangle(img, (x + 250, y), (w + 250, h), (150, 150, 150), cv2.FILLED)
    #          cv2.putText(img, "off", (X + 250, Y), cv2.FONT_HERSHEY_PLAIN,
     #                       5, (0, 255, 255), 5)

        if x + 500 < fx < x + 405 + w and y < fy < y + h - 95: #500 - 95 = 405
            counter_G += 1
     #       cv2.rectangle(img, (x + 500, y), (w + 500, h), (255, 255, 0), cv2.FILLED)
            if counter_G == 1:
                G_on = not G_on

        else:
            counter_G = 0
            if G_on:
                G_val = 1
    #            cv2.rectangle(img, (x + 500, y), (w + 500, h), (0, 255, 0), cv2.FILLED)
    #            cv2.putText(img, "on", (X + 500, Y), cv2.FONT_HERSHEY_PLAIN,
    #                       5, (255, 255, 255), 5)
                print(1)
            else:
                G_val = 0
    #            cv2.rectangle(img, (x + 500, y), (w + 500, h), (150, 150, 150), cv2.FILLED)
     #           cv2.putText(img, "off", (X + 500, Y), cv2.FONT_HERSHEY_PLAIN,
     #                       5, (0, 255, 0), 5)


    
 #       board.digital[pinR].write(R_val)
 #       board.digital[pinY].write(Y_val)
 #       board.digital[pinG].write(G_val)


    #cv2.imshow("Image", img)
    #cv2.waitKey(1)

'''
