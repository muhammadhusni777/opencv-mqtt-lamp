import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

fx_dot = 0
fy_dot = 450
percentage = 0

fx_active = 0
fy_active = 0

sensor = 0
e = 0
e_prev = 0
kp = 5
p_control = 0
ki = 0.5
i_control = 0
kd = 1
d_control = 0
if cap.isOpened() == False:
    print("error")
    exit()



detector  = HandDetector(detectionCon=0.7)

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    imList, bboxInfo = detector.findPosition(img)
    #print(imList)
    ######Setpoint ZONE
    #ball zone
    cv2.rectangle(img, (200, 10),(300, 450), (255, 0, 90), 3)
    #hand zone setting
    cv2.rectangle(img, (0, 0),(450, 500), (255, 0, 90), 3)
    cv2.putText(img, str("MQTT PID BALL LEVITATION"), (350, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    cv2.circle(img, (250, fy_dot), 30, (0, 0, 255), cv2.FILLED)
    cv2.putText(img, str("SETPOINT BALL"), (0, 500), cv2.FONT_HERSHEY_PLAIN, 2.5, (0,0,0), 3)
    cv2.putText(img, str("SETTING ZONE"), (250, 550), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 90), 2)
    cv2.putText(img, str("value : "), (0, 600), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    cv2.putText(img, str(round(percentage,1)), (200, 600), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    
    percentage = (-0.2439 * fy_dot) + 109.76
    
    
    #PID CALCULATION
    e = percentage - sensor
    p_control = kp*e
    i_control = i_control+(ki*e*0.1)
    d_control = ki*(e-e_prev)/0.1
    e_prev = e
    #PID DISPLAY
    cv2.putText(img, str("sensor : "), (800, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    sensor = (0.99*sensor) + (0.01*percentage)
    cv2.putText(img, str(round(sensor,1)), (1000, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    
    cv2.putText(img, str("proportional control : "), (700, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    cv2.putText(img, str(round(p_control,1)), (1100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    
    cv2.putText(img, str("integral control : "), (700, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    cv2.putText(img, str(round(i_control,1)), (1100, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    
    cv2.putText(img, str("derivative control : "), (700, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    cv2.putText(img, str(round(d_control,1)), (1100, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 250), 2)
    ###PID ZONE    
    cv2.rectangle(img, (700, 50),(1200, 350), (0, 255, 255), 2)
    
    if imList:
        fx_active, fy_active = imList[0][0], imList[0][1]
        cv2.putText(img, str("active hand"), (fx_active, fy_active + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        fx, fy = imList[8][0], imList[8][1]
        fx_dot = fx
        
        if (fx < 500 and fx > 100) and fy < 450:
            fy_dot = fy
            if fy_dot > 450 :
                fy_dot = 450
            if fy_dot < 40 :
                fy_dot = 40
            posFinger = [fx, fy]
            
         
        
    cv2.imshow("image", img)
    cv2.waitKey(1)
