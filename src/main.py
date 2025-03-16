import cv2
import numpy as np 
import time 
import hand_tracking as htm
import volume_control as vc

volume = vc.VolumeController()
detector = htm.Hand_Detection()

w , h = 640 , 480
check_volume = False 
last_toggle_time = 0

cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

while True:
    start = time.time()
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    roi_volume = frame[w - 50 : w, 0 : 50]
    frame = detector.findHands(frame)
    lmList = detector.findPos(frame, draw=False)
    if len(lmList) != 0:
        x1 , y1 = lmList[8][1] , lmList[8][2]
        cv2.circle(frame, (x1 , y1), 10, (255, 0, 255), cv2.FILLED)
        current_time = time.time()
        if (lmList[8][1] > w - 50 and lmList[8][1] < w and 
            lmList[8][2] < 50 and lmList[8][2] > 0 and
            ((current_time - last_toggle_time) > 0.5)
        ):
            check_volume = not check_volume
            last_toggle_time = current_time

        
    if check_volume:
        cv2.rectangle(frame, (w - 50, 0), (w, 50), (255, 255, 0), -1)
        cv2.putText(frame, 'Volume', (w - 45, 30), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 1)
        if len(lmList) != 0: 
            frame = volume.controlVolume(lmList, frame)
    else:
        cv2.rectangle(frame, (w - 50, 0), (w, 50), (0, 255, 0), 2)
        cv2.putText(frame, 'Volume', (w - 45, 30), cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 255, 0), 1)
    fps = 1 / (time.time() - start)
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()