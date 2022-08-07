import cv2
import mediapipe as mp
import time

class HandTracking(): 
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.handsMp = mp.solutions.hands

        self.hands = self.handsMp.Hands()
        #self.hands = self.handsMp.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        
        self.drawMp = mp.solutions.drawing_utils

        
    def get_kpts_list(self, img, 
                        draw_keypoints=True): #per frame
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(img_rgb) #get results
        #print('results.multi_hand_landmarks', results.multi_hand_landmarks)
        
        # Restructuring the keypoints for easy access

        multi_subjects_keypoints = [] #(21, 3)
        if results.multi_hand_landmarks:
            for handlm in results.multi_hand_landmarks:
                #print('handlm', handlm)
                #keypoints = []
                for id, joint_lm in enumerate(handlm.landmark):
                    if draw_keypoints:
                       self.drawMp.draw_landmarks(img, handlm, self.handsMp.HAND_CONNECTIONS)

                    h, w, c = img.shape
                    cx, cy = int(joint_lm.x * w), int(joint_lm.y * h)
                    multi_subjects_keypoints.append([id, cx, cy])
                #multi_subjects_keypoints.append(keypoints)
        
        return multi_subjects_keypoints 

        #ex: keypoints_list is [[0, 155, 717], [1, 249, 699], [2, 335, 651], [3, 381, 586], [4, 408, 519], [5, 288, 532], [6, 349, 438], [7, 391, 379], [8, 429, 334], [9, 222, 506], [10, 262, 377], [11, 297, 295], [12, 326, 232], [13, 153, 509], [14, 173, 390], [15, 195, 307], [16, 215, 241], [17, 86, 535], [18, 62, 443], [19, 47, 382], [20, 33, 326]]
        #multi_subjects_keypoints contains other landmarks


    # Returns an x, y pixel value for keypoints. The origin (0,0) is on the upper left corner
    def get_finger_kpts(self, keypoints_list, id):
        if keypoints_list == []:
            return None, None
        else:
            x = keypoints_list[id][1]
            y = keypoints_list[id][2]
            #print(id, keypoints_list)
            assert id == keypoints_list[id][0], print("finger id not matched get_finger_positions")
            

            return x, y
