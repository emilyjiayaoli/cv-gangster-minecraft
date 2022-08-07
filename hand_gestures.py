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
        if self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and self.middleFingIn() and self.thumbFingIn():
            return True
        else: False
        
    def a(self): # left - peace sign
        if not self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and not self.middleFingIn() and self.thumbFingIn():
            return True
        else: False

    def s(self): # down - ring and pinky down
        if not self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and not self.middleFingIn() and not self.thumbFingIn():
            return True
        else: False

    def d(self): # right - four
        if not self.indexFingIn and not self.ringFingIn() and not self.pinkieFingIn() and not self.middleFingIn() and self.thumbFingIn():
            return True
        else: False

    def space(self): # raises the middle finger
        if self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and not self.middleFingIn():
            return True
        else: False     
  
    def l_click(self): # left_click - pinky thumb
        if self.indexFingIn and self.ringFingIn() and not self.pinkieFingIn() and self.middleFingIn() and not self.thumbFingIn():
            return True
        else: False
        
    def r_click(self): # right_click - 4th finger down
        if not self.indexFingIn and self.ringFingIn() and not self.pinkieFingIn() and not self.middleFingIn() and not self.thumbFingIn():
            return True
        else: False
    
    def e(self): # inventory - fist
        if self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and self.middleFingIn() and self.thumbFingIn():
            return True
        else: False
    
    def q(self): # drop item - L with index/thumb
        if not self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and self.middleFingIn() and not self.thumbFingIn():
            return True
        else: False

    def inventory_scroll(self): # - thumbs points left
        if self.indexFingIn and self.ringFingIn() and self.pinkieFingIn() and self.middleFingIn() and not self.thumbFingIn():
            return True
        else: False

    def cursor(): 
        pass
        

#wasd, e (inventory), spacebar, left_key, right_key, inventory_scroll, cursor,