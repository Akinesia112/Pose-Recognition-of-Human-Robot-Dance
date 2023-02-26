from time import time
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import socket
import time
from mediapipe.framework.formats import landmark_pb2

mp_drawing = mp.solutions.drawing_utils #畫出骨架點
mp_pose = mp.solutions.pose #姿態估計的功能（.solutions.pose）

#def UDP (IP, 通道, 傳送的東西):
def UDP (IP, port,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
    b = bytes(message, 'utf-8')
    sock.sendto(b, (IP, port))
    print(b)


# VIDEO FEED
cap = cv2.VideoCapture(0) #0代表camera
## Setup mediapipe instance
## Pose進行辨識
#confidence 0.5
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as  pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        ##偵測結果
        results = pose.process(image)
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        # Extract landmarks
        try:
             landmarks = results.pose_landmarks.landmark
              
        except:
              pass
        
        keypoints=[]
        #要擷取座標點的XYZ
        keypoints.append({
                         landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y,
                         landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].z,
                         })
        #合成為一個字串
        str1 = ''.join(str(e) for e in keypoints)
        print(str1)
##通訊   
       
        UDP ("192.168.237.1",4000,str1)        #利用UDP傳座標字串出去

        # Render detections
        ##底圖 節點 節點連接
        #繪製骨架點
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        time.sleep(0.05)
        cv2.imshow('Mediapipe Feed', image)
        #按Q關閉視窗
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
  




