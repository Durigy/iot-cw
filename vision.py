import time
import cv2 as cv
import mediapipe as mp
#import mediapiperpi4 as mp
from collections import Counter

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

fingercount = 0

cap = cv.VideoCapture(0)

SAMPLES_COUNT = 0
input_samples = []

def normalizeFingerCount(fingercount):
    global input_samples
    # collect input samples (for error correction)
    if len(input_samples) < 4:
        input_samples.append(fingercount)
        return

    # next_digit will be determined based on input_samples
    next_digit = 0

    next_digit = Counter(input_samples).most_common(1)[0][0]
    print(next_digit)

    input_samples = []

    return next_digit

distance_thresholds = {'thumb': 1.2, 'index': 2, 'middle': 2, 'ring': 2, 'pinky': 2}

def detectFingersUp(res, frame):
    
    lms = res.multi_hand_landmarks[0]
    mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS)

    z = lms.landmark[mp_hands.HandLandmark.WRIST].z
    fingercount = 5

    # n is distance between index and pinky mcp points for reference
    n = abs(lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x - lms.landmark[mp_hands.HandLandmark.PINKY_MCP].x)

    if abs(lms.landmark[mp_hands.HandLandmark.THUMB_TIP].x - lms.landmark[mp_hands.HandLandmark.PINKY_MCP].x) <= distance_thresholds['thumb']*n:
        fingercount -= 1
    if abs(lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y - lms.landmark[mp_hands.HandLandmark.WRIST].y) <= distance_thresholds['index']*n:
        fingercount -= 1
    if abs(lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y - lms.landmark[mp_hands.HandLandmark.WRIST].y) <= distance_thresholds['middle']*n:
        fingercount -= 1
    if abs(lms.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y - lms.landmark[mp_hands.HandLandmark.WRIST].y) <= distance_thresholds['ring']*n:
        fingercount -= 1
    if abs(lms.landmark[mp_hands.HandLandmark.PINKY_TIP].y - lms.landmark[mp_hands.HandLandmark.WRIST].y) <= distance_thresholds['pinky']*n:
        fingercount -= 1

    return fingercount

def main():
    while True:

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = hands.process(frame)

        if res.multi_hand_landmarks:
            fingercount = detectFingersUp(res, frame)
            password_digit = normalizeFingerCount(fingercount)
            cap.release()
            print(password_digit)
            return password_digit

        #cv.imshow('output', cv.cvtColor(frame, cv.COLOR_RGB2BGR))

        # if cv.waitKey(1) == 'q':
        #     break
            # identifyPassword(fingercount)

        # cv.imshow('output', cv.cvtColor(frame, cv.COLOR_RGB2BGR))

        # if cv.waitKey(1) == 'q':
        #     break

    # cap.release()
    #cv.destroyAllWindows()
