from mediapipe import mediapipe as mp

from functions import *

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

destroyables = []
draw = FixedStack(5)
health = 3
interval = 0

while True:
    interval += 1
    ret, img = cap.read()
    if not ret:
        continue
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            points = list(handLms.landmark)
            finger = points[8]
            if finger is None:
                continue
            draw.push((finger, interval))

    for pos, xInterval in draw.items:
        drawCircle(img, pos, color=(0, 255, 255))
        if interval - xInterval > 3:
            draw.items.remove((pos, xInterval))
        else:
            for obj in destroyables:
                if obj.isInArea(pos.x * w, pos.y * h):
                    if obj.isBomb:
                        health -= 1
                    destroyables.remove(obj)

    for i in range(10):
        if len(destroyables) < 3:
            if random.randint(0, 10) < 2:
                x = None
                y = None
                while x is None or y is None or (findDestroyables(x, y) is not None):
                    x = random.randint(0, w)
                    y = h - random.randint(0, 30)

                r = random.randint(15, 25)
                bomb = random.randint(0, 10) <= 2
                if random.randint(0, 2) == 0:
                    obj = DestroyableCircle(x, y, r, bomb)
                else:
                    obj = DestroyableRect(x, y, r, bomb)
                destroyables.append(obj)
    for obj in destroyables:
        if obj.cy <= 5:
            if not obj.isBomb:
                health -= 0
            destroyables.remove(obj)
        else:
            obj.cy -= 5
            obj.draw(img)
    if health <= 0:
        break
    for i in range(health):
        drawHearth(img, Point(25 + i * 100, 25))

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
