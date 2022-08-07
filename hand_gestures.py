
from pickle import FALSE


class Hand_Gestures():
    def __init__(self, keypoints):
        self.keypoints = keypoints

    def thumbFingIn(self):
        if self.keypoints[4][1]>self.keypoints[3][1]:
            return True
        else: 
            return False

    def indexFingIn(self):
        if self.keypoints[8][2]>self.keypoints[7][2]:
            return True
        else: 
            return False

    def middleFingIn(self):
        if self.keypoints[12][2]>self.keypoints[11][2]:
            return True

        else:
            return False
            
    def ringFingIn(self):
        if self.keypoints[16][2]>self.keypoints[15][2]:
            return True
        else:
            return False

    def pinkieFingIn(self):
        if self.keypoints[12][2]>self.keypoints[11][2]:
            return True
        else:
            return False

    def handClosed(self):
        # Return True if hand gestures is open = clicking
            # pt 12<11 (middle finger), pt 16<15 (ring finger)
        if self.keypoints == []:
            return False
        else:
            if self.keypoints[11][2]>self.keypoints[12][2] and self.keypoints[15][2]>self.keypoints[16][2]:
                return True
            else:
                return False
            
    def indexRingFingersDown(self):
        if self.indexFingIn() and self.middleFingIn():
            return True
        else:
            return False

    def w(self): # up - okay sign
        pass
        
    def a(self): # left - peace sign
        pass

    def s(self): # down - west coast
        pass

    def d(self): # right - westside
        pass

    def space(self): # raises the middle finger
        if self.indexFingIn and self.ringFingIn() and self.ringFingIn() and not self.middleFingIn():
            return True
        else: False     
    

    def l_click(self): # left_click - pinky thumb
        pass
        
    def r_click(self): # right_click - 4th finger down
        pass
    
    def e(self): # inventory - fist
        pass
    
    def q(self): # drop item - thumbs up
        pass
    def inventory_scroll(self): # - thumbs down
        pass

    def cursor(): 
        pass

        

#wasd, e (inventory), spacebar, left_key, right_key, inventory_scroll, cursor,


    
