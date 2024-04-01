import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0, trackCon=0.5):
        self.res = None
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img, draw=True):
        img = cv2.flip(img, 2)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(imgRGB)
        if self.res.multi_hand_landmarks:
            for handLms in self.res.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []

        if self.res.multi_hand_landmarks:
            myHand = self.res.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                # print(id, cx, cy)

                if draw: pass
                # cv2.circle(img, (cx, cy), 1, (255, 255, 0), cv2.FILLED)

        return lmList


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        _, img = cap.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            pass
            # print(lmList[4])

        cv2.imshow("Imagem", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
