# Author: Kimi Heinonen
# This is simple script to record screen with the option to record audio

import cv2
import pyaudio
import numpy as np
import pyautogui
from PIL import ImageGrab

MAX_SIZE = pyautogui.size()
BBOX = (800, 600)
REGION = (0, 0, BBOX[0], BBOX[1])
RECORD = False
INC = 10
FRAMES = 60.0

def handle_key(key, frame, out):
    global BBOX, RECORD, REGION
    if key == ord("r"):
        RECORD = True
        print("STARTED RECORDING")
    elif key == ord("p"):
        RECORD = False
    elif key == ord("q") or key == ord("s"):
        return True
    if RECORD:
        out.write(frame)
        return False
    elif key == ord("x"):
        BBOX = (BBOX[0] - INC, BBOX[1])
        REGION = (0, 0, BBOX[0], BBOX[1])
    elif key == ord("X"):
        BBOX = (BBOX[0] + INC, BBOX[1])
        REGION = (0, 0, BBOX[0], BBOX[1])
    elif key == ord("y"):
        BBOX = (BBOX[0], BBOX[1] - INC)
        REGION = (0, 0, BBOX[0], BBOX[1])
    elif key == ord("Y"):
        BBOX = (BBOX[0], BBOX[1] + INC)
        REGION = (0, 0, BBOX[0], BBOX[1])
    elif key == ord("4"):
        r = list(REGION)
        r[0] -= INC
        r[2] -= INC
        REGION = tuple(r)
    elif key == ord("8"):
        r = list(REGION)
        r[1] -= INC
        r[3] -= INC
        REGION = tuple(r)
    elif key == ord("6"):
        r = list(REGION)
        r[0] += INC
        r[2] += INC
        REGION = tuple(r)
    elif key == ord("2"):
        r = list(REGION)
        r[1] += INC
        r[3] += INC
        REGION = tuple(r)
    elif key == ord("f") or key == ord("F"):
        if BBOX == MAX_SIZE:
            BBOX = (int(MAX_SIZE[0] / 2), int(MAX_SIZE[1] / 2))
            REGION = (0, 0, BBOX[0], BBOX[1])
        else:
            BBOX = MAX_SIZE
            REGION = (0, 0, BBOX[0], BBOX[1])
    return False

def videorecord_wrapper():
    fourcc = cv2.VideoWriter_fourcc(*"FMP4")
    out = cv2.VideoWriter("output.avi", fourcc, FRAMES, BBOX, True)
    return out

if __name__ == "__main__":
    out = videorecord_wrapper()

    while True:
        img = ImageGrab.grab(bbox=REGION)
        img = np.array(img)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        key = cv2.waitKey(1) & 0xFF
        if handle_key(key, frame, out):
            break
        cv2.imshow("foo", frame)

cv2.destroyAllWindows()
out.release()