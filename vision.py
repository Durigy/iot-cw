import cv2 as cv
from collections import Counter
# import matplotlib
# matplotlib.use('Agg')
# import gi
# gi.require_version('Gtk', '2.0')

def normalizeFingerCount(fingercount, input_samples, SAMPLES_COUNT, MIN_SAMPLES):

    # collect input samples (for error correction)
    if SAMPLES_COUNT <= MIN_SAMPLES:
        input_samples.append(fingercount)
        return

    # next_digit will be determined based on input_samples
    next_digit = 0

    next_digit = Counter(input_samples).most_common(1)[0][0]

    input_samples = []

    return next_digit


def detectFingersUp(res, frame, mp_hands, mp_draw, distance_thresholds):
    
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

def get_finger_count(mp_hands, mp_draw, hands):
    
    cap = cv.VideoCapture(1)

    SAMPLES_COUNT = 0
    MIN_SAMPLES = 3
    input_samples = []

    distance_thresholds = {'thumb': 1.2, 'index': 2, 'middle': 2, 'ring': 2, 'pinky': 2}

    password_digit = None

    while SAMPLES_COUNT <= MIN_SAMPLES:

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = hands.process(frame)

        if res.multi_hand_landmarks:
            fingercount = detectFingersUp(res, frame, mp_hands, mp_draw, distance_thresholds)
            SAMPLES_COUNT += 1
            password_digit = normalizeFingerCount(fingercount, input_samples, SAMPLES_COUNT, MIN_SAMPLES)

            if password_digit is None:
                continue
            else:
                break

        # cv.imshow('output', cv.cvtColor(frame, cv.COLOR_RGB2BGR))
        # cv.waitKey()
        
    cap.release()
    
    return password_digit


    #     cv.imshow('output', cv.cvtColor(frame, cv.COLOR_RGB2BGR))

    # cap.release()
    # cv.destroyAllWindows()

if __name__ == "__main__":
    import mediapipe as mp

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

    while True:
        print(get_finger_count(mp_hands, mp_draw, hands))