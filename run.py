import cv2
from hand_tracker import HandTracker
from subprocess import Popen,PIPE
from subprocess import call
import pyautogui
WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "./palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "./hand_landmark.tflite"
ANCHORS_PATH = "./anchors.csv"

POINT_COLOR = (0, 0, 255)
CONNECTION_COLOR = (0, 255, 0)
THICKNESS = 1
l = []
xp,yp = [],[]
cv2.namedWindow(WINDOW)
capture = cv2.VideoCapture(0)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

if capture.isOpened():
    hasFrame, frame = capture.read()
else:
    hasFrame = False

#        8   12  16  20
#        |   |   |   |
#        7   11  15  19
#    4   |   |   |   |
#    |   6   10  14  18
#    3   |   |   |   |
#    |   5---9---13--17
#    2    \         /
#     \    \       /
#      1    \     /
#       \    \   /
#        ------0-
connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (5, 6), (6, 7), (7, 8),
    (9, 10), (10, 11), (11, 12),
    (13, 14), (14, 15), (15, 16),
    (17, 18), (18, 19), (19, 20),
    (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)
]

detector = HandTracker(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.3
)
#        8   12  16  20
#        |   |   |   |
#        7   11  15  19
#    4   |   |   |   |
#    |   6   10  14  18
#    3   |   |   |   |
#    |   5---9---13--17
#    2    \         /
#     \    \       /
#      1    \     /
#       \    \   /
#        ------0-
def action_detector(points):
    for z in points:
        x, y = z
        xp.append(x)
        yp.append(y)
    diffx4_8 = int(xp[4]-xp[8])
    diffy4_8 = int(yp[4]-yp[8])
    diffy8_6 = int(yp[8]-yp[6])
    diffy12_10 = int(yp[12]-yp[10])
    diffy16_13 = int(yp[16]-yp[13])
    diffy20_17 = int(yp[20]-yp[17])
    if abs(diffx4_8) < 3 and abs(diffy4_8) < 3:
        print("Ohhh. Thumb and index touchy tuchy")
    elif diffy8_6> 0:
        if diffy12_10 < 0 and diffy16_13 < 0 and diffy20_17 < 0:
            pyautogui.leftClick()
    elif diffy12_10> 0:
        if diffy8_6 < 0 and diffy16_13 < 0 and diffy20_17 < 0:
            pyautogui.rightClick()
    
    xp.clear()
    yp.clear()

def x():
    xf2,yf2 = points[12]
    xb2,yb2 = points[9]
    diff_fing2 = yf2-yb2
    diff_fing2 = abs(diff_fing2)
    if diff_fing2 < 10:
        print("Click detected")
while capture.isOpened():
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image,1)
    points, _ = detector(image)
    frame = cv2.flip(frame,1)
    if points is not None:
        for point in points:
            x, y = point
            cv2.circle(frame, (int(x), int(y)), 2, POINT_COLOR, THICKNESS)
        action_detector(points)
        for connection in connections:
            x0, y0 = points[connection[0]]
            x1, y1 = points[connection[1]]
            cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), CONNECTION_COLOR, THICKNESS)
#Moving Mouse
        l.append(points[0])
        if len(l)>2:
            prevx,prevy = l.pop(0)
            cx, cy = points[0]
            msg = str.encode('mousermove '+str(int((cx-prevx)*4))+" "+str(int((cy-prevy)*4))+" ")
            p = Popen(['xte'],stdin=PIPE)
            p.communicate(input=msg)
    cv2.imshow(WINDOW, frame)
  #  action_detector(points)
    hasFrame, frame = capture.read()
    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
