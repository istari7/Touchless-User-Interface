import cv2
from hand_tracker import HandTracker
from subprocess import Popen,PIPE
from subprocess import call

WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "./palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "./hand_landmark.tflite"
ANCHORS_PATH = "./anchors.csv"

POINT_COLOR = (0, 0, 255)
CONNECTION_COLOR = (0, 255, 0)
THICKNESS = 1
l = []
