import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

import math

fx=0
fy=0

fx1=0
fy1=0

fx2=0
fy2=0

fx3=0
fy3=0

fx4=0
fy4=0

fx5=0
fy5=0

fx6=0
fy6=0

fx7=0
fy7=0

fx8=0
fy8=0
mouth_x=0
mouth_y=0

l_eye_val = 0
r_eye_val = 0
fx9 = 0
fy9 = 0

fx10=0
fy10=0

cap = cv2.VideoCapture(0)
cap.set(3,800)
cap.set(4,720)
detector = FaceMeshDetector(0.7)
while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img)
    #cv2.putText(img, str("SETPOINT BALL"), (0, 500), cv2.FONT_HERSHEY_PLAIN, 2.5, (0,0,0), 3)
    if faces:
        fx,fy=faces[0][410]
        fx1,fy1 = faces[0][186]
        fx2,fy2 = faces[0][0]
        fx3,fy3 = faces[0][17]
        fx4,fy4 = faces[0][378]
        fx5,fy5 = faces[0][159]
        fx6,fy6 = faces[0][145]
        fx7,fy7 = faces[0][386]
        fx8,fy8 = faces[0][374]
        
        fx9,fy9 = faces[0][234]
        
        fx10,fy10 = faces[0][347]
        #print(faces[0][30])
        
        #cv2.circle(img, (fx, fy), 10, (0, 0, 0), cv2.FILLED)
        #cv2.circle(img, (fx1, fy1), 10, (0, 0, 0), cv2.FILLED)
        cv2.line(img, (fx, fy),(fx1, fy1), (255, 255, 255), 3)
        mouth_x = math.sqrt(pow((fx1 - fx), 2) + pow((fy1 - fy), 2))
        mouth_y = math.sqrt(pow((fx3 - fx2), 2) + pow((fy3 - fy2), 2))
        l_eye_val = math.sqrt(pow((fx5 - fx6), 2) + pow((fy5 - fy6), 2))
        r_eye_val = math.sqrt(pow((fx7 - fx8), 2) + pow((fy7 - fy8), 2))
        
        print(fx4)
        print(fy4)
        #print(mouth_y)
        cv2.line(img, (fx2, fy2),(fx3, fy3), (255, 255, 255), 3)
        
        cv2.putText(img, str("x mulut :"), (fx4, fy4), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        cv2.putText(img, str(round(mouth_x,0)), (fx4 + 80, fy4), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        
        cv2.putText(img, str("y mulut :"), (fx4, fy4+20), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        cv2.putText(img, str(round(mouth_y,0)), (fx4 + 80, fy4+20), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        
        cv2.putText(img, str("L eye val :"), (fx9, fy9), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        cv2.putText(img, str(round(l_eye_val,0)), (fx9, fy9 +20), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        
        cv2.putText(img, str("R eye val :"), (fx10, fy10), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        cv2.putText(img, str(round(r_eye_val,0)), (fx10, fy10+20), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
        
        cv2.line(img, (fx5, fy5),(fx6, fy6), (255, 255, 255), 3)
        cv2.line(img, (fx7, fy7),(fx8, fy8), (255, 255, 255), 3)
        
        if ((mouth_x > 80) and (mouth_y > 50) and (l_eye_val < 12) and (r_eye_val < 12) ) :
            cv2.putText(img, str("api api teu stress"), (0, 100), cv2.FONT_HERSHEY_PLAIN, 2.5, (255,0,0), 3)
            #cv2.putText(img, str("SMILE"), (0, 0), cv2.FONT_HERSHEY_PLAIN, 2.5, (0,0,0), 3)
            print("api api teu stress")
        else:
            cv2.putText(img, str("stress pisan"), (0, 100), cv2.FONT_HERSHEY_PLAIN, 2.5, (0,0,255), 3)
            #cv2.putText(img, str("NO SMILE"), (0, 0), cv2.FONT_HERSHEY_PLAIN, 2.5, (0,0,0), 3)
            print("stress")
    cv2.imshow("stress detector", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
