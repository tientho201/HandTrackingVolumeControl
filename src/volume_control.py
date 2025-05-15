import numpy as np 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2

class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers() # Lấy thiết bị phát âm thanh mặc định
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # Kích hoạt thiết bị phát âm thanh
        self.volume = interface.QueryInterface(IAudioEndpointVolume) # Trả về giao diện IAudioEndpointVolume
        # volume.GetMute() #  Kiểm tra xem thiết bị có đang bị tắt tiếng không
        # volume.GetMasterVolumeLevel() # Lấy mức âm lượng hiện tại (dB)
        # volume.GetVolumeRange() # Lấy phạm vi âm lượng có thể điều chỉnh
        # self.volume.SetMasterVolumeLevel(-10.0, None) # Đặt mức âm lượng (dB)
    def setVolume_Bar_Per(self, hand_distance , min_dist = 20 , max_dist = 200 , minBar = 400 , maxBar = 200):
        '''
            This function is used to calculate the volume level and the volume level display bar
            hand_distance : Distance between thumb and index finger
            min_dist : Minimum distance
            max_dist : Maximum distance
            minBar : Minimum value of the volume level display bar
            maxBar : Maximum value of the volume level display bar  
        '''
        volBar = np.interp(hand_distance, [min_dist, max_dist], [minBar, maxBar])
        volPer = np.interp(hand_distance, [min_dist, max_dist], [0, 100])
        volScalar = np.interp(volPer, [0, 100], [0.0, 1.0])
        self.volume.SetMasterVolumeLevelScalar(volScalar, None)
        return int(volPer) , int(volBar) 

    def controlVolume(self , lmList: list , frame: np.ndarray , min_dist = 20 , max_dist = 200 , minBar = 400 , maxBar = 200 ):
        '''
            This function is used to control the volume level
            lmList : List of landmarks
            frame : Image frame
            min_dist : Minimum distance
            max_dist : Maximum distance
            minBar : Minimum value of the volume level display bar
            maxBar : Maximum value of the volume level display bar
        '''        
    
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2  ,y2 = lmList[8][1] , lmList[8][2]
        cx , cy = (x1 + x2) // 2 , (y1 + y2) // 2
        
        distance = np.sqrt(( x1 - x2 )**2 + (y1 - y2)**2)
        
        cv2.circle(frame, (x1,y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2 , y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(frame,(x1,y1),(x2 , y2) ,  (0, 255, 0), 3)
        cv2.circle(frame, (cx , cy), 10, (255, 0, 255), cv2.FILLED)
        
        volPer , volBar =  self.setVolume_Bar_Per(distance , min_dist , max_dist , minBar , maxBar)
        
        if distance < 30:
            cv2.line(frame,(x1,y1),(x2 , y2) ,  (255, 0, 255), 3)
            cv2.circle(frame, (cx , cy), 10, (0, 255, 0), cv2.FILLED)
    
        cv2.rectangle(frame, (50, 200), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(frame, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        return frame

class MonitorController:
    def __init__(self):
        pass