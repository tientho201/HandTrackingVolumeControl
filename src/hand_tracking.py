import cv2
import numpy as np
import time
import mediapipe as mp

class Hand_Detection():
    def __init__(self , maxHand = 2 , detectionCon = 0.7, trackCon = 0.5):
        self.maxHand = maxHand
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False, 
            max_num_hands =  self.maxHand , 
            model_complexity=1, 
            min_detection_confidence = self.detectionCon , 
            min_tracking_confidence = self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
   
    # Hàm tìm kiếm bàn tay     
    def findHands(self , img , draw = True):
        imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img , handLms , self.mpHands.HAND_CONNECTIONS , 
                                               self.mpDraw.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                               self.mpDraw.DrawingSpec(color=(250,44,250), thickness=2, circle_radius=2))
        return img
    
    def findPos(self , img , handNo = 0 , draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            # myHnad.landmark chứa 21 điểm mốc của bàn tay do MediaPipe Hands nhận diện được.
            # Mỗi lm là một đối tượng NormalizedLandmark chứa tọa độ (x, y, z) của một điểm mốc trong không gian chuẩn hóa.
            for id , lm in enumerate(myHand.landmark):
                h , w , c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                lmList.append([id , cx , cy])
                if draw:
                    cv2.circle(img , (cx , cy) , 15 , (255 , 0 , 255) , cv2.FILLED)
        return lmList
    
