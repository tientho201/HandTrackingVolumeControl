import cv2
import numpy as np 
import time 
import src.hand_tracking as htm
import src.volume_control as vc
import pyautogui  

volume = vc.VolumeController()
detector = htm.Hand_Detection()

screen_w, screen_h = pyautogui.size()

# w , h =   1280, 720
w , h =   640, 480
check_volume = False 
check_Drag_Drop = False
last_toggle_time = 0

cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

window_x = (screen_w - w) // 2   # Canh giữa theo chiều ngang
window_y = (screen_h - h) // 2 - 30

cell_size = 100

while True:
    start = time.time()
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    frame = detector.findHands(frame)
    lmList = detector.findPos(frame, draw=False)
    
    if len(lmList) != 0:
        x1 , y1 = lmList[8][1] , lmList[8][2]
        cv2.circle(frame, (x1 , y1), 10, (255, 0, 255), cv2.FILLED)
        current_time = time.time()
        if (x1 > w - cell_size and x1 < w and 
            y1 < cell_size and y1 > 0 and
            ((current_time - last_toggle_time) > 0.5)
        ):
            check_volume = not check_volume
            last_toggle_time = current_time
        elif (x1 > w - 2*cell_size and x1 < w - cell_size and 
            y1 < cell_size and y1 > 0 and
            ((current_time - last_toggle_time) > 0.5)
        ):
            check_Drag_Drop = not check_Drag_Drop
            last_toggle_time = current_time

        
    if check_volume:
        cv2.rectangle(frame, (w - cell_size, 0), (w, cell_size), (255, 255, 0), -1)
        cv2.putText(frame, 'Volume', (w - cell_size + cell_size // 4 , cell_size // 2), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 1)
        if len(lmList) != 0: 
            frame = volume.controlVolume(lmList, frame)
    else:
        cv2.rectangle(frame, (w - cell_size, 0), (w, cell_size), (0, 255, 0), 2)
        cv2.putText(frame, 'Volume', (w - cell_size + cell_size //4 , cell_size // 2), cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 255, 0), 1)
    
        
        
    fps = 1 / (time.time() - start)
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
    cv2.imshow('frame', frame)
    
    # Di chuyển cửa sổ "Camera" ra giữa màn hình
    cv2.moveWindow('frame', window_x, window_y)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()