from operator import index
import cv2
import mediapipe as mp
import time
import hand_tracking_module as htm
import hand_gestures_old as hg
import numpy as np

'''
# Specify location of 3x3 squares
GRID = {1:[(200,100),(400,300)], #first point in rectangle, second point in rectangle
            2:[(400,100),(600,300)], 
            3:[(600,100),(800,300)], 
            4:[(200,300),(400,500)], 
            5:[(400,300),(600,500)],
            6:[(600,300),(800,500)],
            7:[(200,500),(400,700)],
            8:[(400,500),(600,700)],
            9:[(600,500),(800,700)],
}
# Specify location of buttons on the screen
BUTTON_SETTINGS = {
    'esc': [(20, 100), (100, 150)], #first point in rectangle, second point in rectangle
    'restart': [(20, 180), (100, 230)],
}

# Translate GRID in x and y direction
transform_val = 100
for i in GRID:
    x = 100 # parameter
    y = -45 # parameter
    cur = GRID[i]
    new_cur = [(cur[0][0]+x,cur[0][1]+y),(cur[1][0]+x,cur[1][1]+y)] #transform x
    GRID[i] = new_cur
'''

# Use OpenCV to draw individual squares
def boardSetUp(img):
    for id in range(1, len(GRID.keys()) + 1):
        img = cv2.rectangle(img, GRID[id][0],GRID[id][1],(255,0,0),4) #1
    cv2.putText(img,"Hand-controlled Tic Tac Toe",(10, 40),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)
    cv2.rectangle(img, BUTTON_SETTINGS['esc'][0], BUTTON_SETTINGS['esc'][1], (255, 0, 0), 4)
    cv2.putText(img,"Quit game",(BUTTON_SETTINGS['esc'][0][0],BUTTON_SETTINGS['esc'][0][1]-6),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.rectangle(img, BUTTON_SETTINGS['restart'][0], BUTTON_SETTINGS['restart'][1], (255, 0, 0), 4)
    cv2.putText(img,"Restart",(BUTTON_SETTINGS['restart'][0][0],BUTTON_SETTINGS['restart'][0][1]-6),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    return img

# Prints out the winner if there is one
def declareWinner(img, winner, draw_status=False): 
    if draw_status == True:
        winner_message = "Winner: No One :("
    else:
        winner_message = "Winner: Player " + str(winner)
    cv2.putText(img, winner_message,(910, 200),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)
    cv2.putText(img, "Please restart the game",(910, 250),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

# If a square is selected, returns the idx of the board and the id for the selected square. 
# If no square is selected (x,y is not not within the bounds of the square), returns h=99, w=99, selected_square=None
def checkInBounds(x,y): 
    h = 99
    w = 99
    selected_square = None
    if GRID[1][0][0] < x < GRID[1][1][0]: #column 1
        if GRID[1][0][1] < y < GRID[1][1][1]:
            h, w, selected_square = 0, 0, 1 #1
        if GRID[4][0][1] < y < GRID[4][1][1]:
            h, w, selected_square = 1, 0, 4 #4
        if GRID[7][0][1] < y < GRID[7][1][1]:
            h, w, selected_square = 2, 0, 7 #7
    if GRID[2][0][0] < x < GRID[2][1][0]:
        if GRID[2][0][1] < y < GRID[2][1][1]:
            h, w, selected_square = 0, 1, 2 #2
        if GRID[5][0][1] < y < GRID[5][1][1]:
            h, w, selected_square = 1, 1, 5 #5
        if GRID[8][0][1] < y < GRID[8][1][1]:
            h, w, selected_square = 2, 1, 8 #8
    if GRID[3][0][0] < x < GRID[3][1][0]:
        if GRID[3][0][1] < y < GRID[3][1][1]:
            h, w, selected_square = 0, 2, 3 #3
        if GRID[6][0][1] < y < GRID[6][1][1]:
            h, w, selected_square = 1, 2, 6 #6
        if GRID[9][0][1] < y < GRID[9][1][1]:
            h, w, selected_square = 2, 2, 9 #9
    print(h, w, selected_square)
    return h, w, selected_square

def updateBoard(board, h, w, selected_square, player1, x, y):
    # Updates the board on the screen according to the square clicked and player played
    # Updates the internal board
    if player1:
        board[h][w] = 1
        # Calculates the center of the box
        first_pt, second_pt = GRID[selected_square][0], GRID[selected_square][1]
        graph_x = int((second_pt[0]+first_pt[0])/2)
        graph_y = int((second_pt[1]+first_pt[1])/2)

        player1 = False
        
    else:
        board[h][w] = 2
        first_pt, second_pt = GRID[selected_square][0], GRID[selected_square][1]
        graph_x = int((second_pt[0]+first_pt[0])/2)
        graph_y = int((second_pt[1]+first_pt[1])/2)

        player1= True

    return board, player1, graph_x, graph_y

def winnerChecker(board, img):
    #check winners in rows
    print(board)
    for row in board:
        if row[0] == row[1] == row[2] == 1:
            winner=1
            return True, winner
        if row[0] == row[1] == row[2] == 2:
            winner=2
            return True, winner
    #check winners in column
    if (board[0][0] != None) & (board[0][0] == board[1][0] == board [2][0] ==1) | (board[0][1] != None) & (board[0][1] == board[1][1] == board [2][1] ==1) | (board[0][2] != None) & (board[0][2] == board[1][2] == board [2][2] ==1):
        winner = 1
        return True, winner
    if (board[0][0] != None) & (board[0][0] == board[1][0] == board [2][0] == 2) | (board[0][1] != None) & (board[0][1] == board[1][1] == board [2][1] == 2) | (board[0][2] != None) & (board[0][2] == board[1][2] == board [2][2] == 2):
        winner = 2
        return True, winner
    #check winners diagonally
    if (board[0][0] != None) & (board[0][0] == board[1][1] == board [2][2] == 1) | (board[0][2] != None)& (board[0][2] == board[1][1] == board [2][0] == 1):
        winner = 1
        return True, winner
    if (board[0][0] != None) & (board[0][0] == board[1][1] == board [2][2] == 2) | (board[0][2] != None) & (board[0][2] == board[1][1] == board [2][0] == 2):
        winner = 2
        return True, winner
    return False, None

def drawChecker(board):
    for r in board:
        for c in r:
            if c == None:
                return False
    return True
    
def keyPressed(key: str, finger_x, finger_y):
    if finger_x == None or finger_y == None:
        return False
    rect_pt1 = BUTTON_SETTINGS[key][0]
    rect_pt2 = BUTTON_SETTINGS[key][1]
    if rect_pt1[0] < finger_x < rect_pt2[0] and rect_pt1[1] < finger_y < rect_pt2[1]:
        return True

def setDefault():
    
    hand = htm.HandTracking()
    cTime = 0
    pTime = 0

    static_overlay = cv2.imread("static_overlay.png")
    static_underlay = cv2.imread("static_overlay.png")

    return hand, cTime, pTime, static_overlay, static_underlay

def checkKeyPressed(img, keypoints, gesture, hand2=False):
    img_h, img_w, img_c = img.shape
    if keypoints != []:
        if hand2: #gestures for hand 2
            if gesture.l_click():
                cv2.putText(img,"l_click",(int(0.85*img_w), int(0.1*img_h)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                print('todo')
            if gesture.r_click():
                cv2.putText(img,"r_click",(int(0.85*img_w), int(0.1*img_h)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        else: #gestures for hand 1
            if gesture.space():
                cv2.putText(img,"space",(int(0.85*img_w), int(0.1*img_h)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                print('todo')
            if gesture.w():
                cv2.putText(img,"w",(int(0.85*img_w), int(0.1*img_h)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            if gesture.a():
                cv2.putText(img,"a",(int(0.85*img_w), int(0.1*img_h)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            if gesture.s():
                print('todo')
            if gesture.d():
                print('todo')
            if gesture.e():
                print('todo')
            if gesture.q():
                print('todo')


def main():
    cap = cv2.VideoCapture(0)
    #cap.set(3, 640)
    #cap.set(4, 480)
    
    hand, cTime, pTime, static_overlay, static_underlay = setDefault()

    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)

        img_h, img_w, img_c = img.shape

        
        #static_underlay = boardSetUp(static_underlay)
        static_underlay = cv2.imread("static_overlay.png") #temporarily

        multi_subjects_keypoints = hand.get_kpts_list(img)
        #print("multi_subjects_keypoints len is ", multi_subjects_keypoints)
        
        if multi_subjects_keypoints != [[]]:
            if len(multi_subjects_keypoints) == 1:
                h1_keypoints = hand.get_kpts_list(img)[0]
                x1, y1 = hand.get_finger_kpts(h1_keypoints, 12) #retrieves x, y position of the index finger for the current frame
                img = cv2.circle(img, (x1, y1), 20, (255, 0, 0),3)
                h1_gesture = hg.Hand_Gestures(h1_keypoints)

                checkKeyPressed(img, h1_keypoints, h1_gesture)
            elif len(multi_subjects_keypoints) == 2:
                h1_keypoints = hand.get_kpts_list(img)[0] #returns list of 21 keypoint positions at that frame
                h2_keypoints = hand.get_kpts_list(img)[1]
                print('h2_keypoints', len(hand.get_kpts_list(img)))
                #h2_keypoints = hand.get_kpts_list(img)[1] 

                x1, y1 = hand.get_finger_kpts(h1_keypoints, 12)
                x2, y2 = hand.get_finger_kpts(h2_keypoints, 12) # x2, y2 at the center of the hand
                img = cv2.circle(img, (x1, y1), 20, (255, 0, 0),3)
                img = cv2.circle(img, (x2, y2), 20, (255, 0, 0),3)
                h1_gesture = hg.Hand_Gestures(h1_keypoints)
                h2_gesture = hg.Hand_Gestures(h2_keypoints)
                
                checkKeyPressed(img, h1_keypoints, h1_gesture)
                checkKeyPressed(img, h1_keypoints, h1_gesture, hand2=True)
            else:
                if len(multi_subjects_keypoints) != 1 and len(multi_subjects_keypoints) !=2:
                    print("multi_subjects_keypoints length is not 1 or 2")

        '''
        if keyPressed('esc', x, y): #if hand is in bounding box of esp key
            break
        if keyPressed('restart', x, y):
            board, hand, cTime, pTime, winner_status, winner, player1, static_overlay, static_underlay = setDefault()
        '''

        
        cTime = time.time()
        fps = 1/(cTime -pTime)
        pTime = cTime
    

        #cv2.putText(img, "FPS:"+str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (230,0,0), 2)
        
        # Prep for image overlay: converting all layers to be BGRA
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        static_overlay = cv2.cvtColor(static_overlay, cv2.COLOR_BGR2BGRA) # The circles
        static_underlay = cv2.cvtColor(static_underlay, cv2.COLOR_BGR2BGRA) # Buttons & permanent text

        combined_mask = cv2.addWeighted(static_overlay, 1, static_underlay, 1, 0)
        img = cv2.addWeighted(combined_mask, 10, img, 0.5, 0)
    
        cv2.imshow("image", img)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
