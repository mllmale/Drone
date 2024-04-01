import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpHand = mp.solutions.hands
hands = mpHand.Hands()

mpDraw = mp.solutions.drawing_utils

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(imgRGB)

    # print(res.multi_hand_landmarks)

    if res.multi_hand_landmarks:
        for handLms in res.multi_hand_landmarks:
            # id é a identificação do lm. Por ex, 4 é polegar
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)

                if id == 4:
                    cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

    cv2.imshow("Imagem", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
