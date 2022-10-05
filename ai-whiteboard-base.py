#Imports 
import cv2
import mediapipe as mp
import time

#Video capture
cap = cv2.VideoCapture(0)

#Variables 
mpHands = mp.solutions.hands
hands = mpHands.Hands()
handDraw = mp.solutions.drawing_utils
fingerY = [0] * 21
fingersUp = [0] * 5
previousTime = 0
currentTime = 0


#Video loop and processing
while True:
    detected, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    #Getting various information about the landmarks on the hand
    if results.multi_hand_landmarks:
        
        for landmarks in results.multi_hand_landmarks:
            handDraw.draw_landmarks(img, landmarks, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(landmarks.landmark):
                height, width, center = img.shape
                centerX, centerY = int(lm.x * width), int(lm.y * height)
                
                fingerY[id] = centerY

                
                # if id == 4:
                #     print(id, fingerY[id])

                # if id == 2:
                #     print(id, fingerY[id])
                
                #Fingertip recognition logic (May need tweaked. Thumb recognition is a little iffy)
                if fingerY[6] > fingerY[8]:
                    fingersUp[0] = 1
                    #print("Index finger up!")
                elif fingerY[6] < fingerY[8]:
                    fingersUp[0] = 0
                    #print ("Index finger down!")
                if fingerY[10] > fingerY[12]:
                    fingersUp[1] = 1
                    #print("Middle finger up!")
                elif fingerY[10] < fingerY[12]:
                    fingersUp[1] = 0
                    #print ("Middle finger down!")
                if fingerY[14] > fingerY[16]:
                    fingersUp[2] = 1
                    #print("Ring finger up!")
                elif fingerY[14] < fingerY[16]:
                    fingersUp[2] = 0
                    #print ("Ring finger down!")
                if fingerY[18] > fingerY[20]:
                    fingersUp[3] = 1
                    #print("Pinky finger up!")
                elif fingerY[18] < fingerY[20]:
                    fingersUp[3] = 0
                    #print ("Pinky finger down!")
                if fingerY[2] - fingerY[4] > 75:
                    fingersUp[4] = 1
                    #print ("Thumb out!")
                else:
                    fingersUp[4] = 0
                    #print("Thumb in!")

                #Case statement to match gestures to functions (Functions may still be tweaked or added)
                match fingersUp:

                    case [0, 0, 0, 0, 0]:
                        print("No gestures detected")
                    case [1,0,0,0,0]:
                        print("Placeholder for draw function")
                    case [1,0,0,0,1]:
                        print("Placeholder for movement function")
                    case [1,1,0,0,0]:
                        print("Placeholder for undo function")
                    case [1,1,1,0,0]:
                        print("Placeholder for save function")

                           
                
    #Code to compute FPS and show on screen
    currentTime = time.time()
    fps = 1/(currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
    
    #Show contents of frame
    cv2.imshow("Frame", img)
    cv2.waitKey(1)

    
