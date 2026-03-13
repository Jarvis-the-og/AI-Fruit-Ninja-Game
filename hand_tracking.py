import cv2
import mediapipe as mp

class HandTracker:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils

    def get_hand_position(self):

        ret, frame = self.cap.read()
        frame = cv2.flip(frame,1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        x,y = None,None

        if result.multi_hand_landmarks:

            for hand in result.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(frame, hand,
                mp.solutions.hands.HAND_CONNECTIONS)

                landmark = hand.landmark[8]

                h,w,_ = frame.shape
                x,y = int(landmark.x*w), int(landmark.y*h)

        cv2.imshow("Camera",frame)
        cv2.waitKey(1)

        return x,y