import cv2 as cv
from collections import Counter
import time
# import matplotlib
# matplotlib.use('Agg')
# import gi
# gi.require_version('Gtk', '2.0')


# turn measurements of fingercount into a password digit
def normalizeFingerCount(fingercount, input_samples, SAMPLES_COUNT, MIN_SAMPLES):

    # collect input samples (for error correction)
    if SAMPLES_COUNT <= MIN_SAMPLES:
        input_samples.append(fingercount)
        return

    # next_digit will be determined based on input_samples
    next_digit = 0

    # most common fingercount number from collected fingercount samples will become the next password digit
    next_digit = Counter(input_samples).most_common(1)[0][0]

    input_samples = []

    return next_digit


def detectFingersUp(res, frame, mp_hands, mp_draw, distance_thresholds):
    
    lms = res.multi_hand_landmarks[0] # extract the processed hand landmarks
    mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS)

    z = lms.landmark[mp_hands.HandLandmark.WRIST].z

    # start with a count of 5 and subtract if a finger is detected to be down
    fingercount = 5

    # n is distance between index and pinky mcp points for reference
    n = abs(lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x - lms.landmark[mp_hands.HandLandmark.PINKY_MCP].x)

    # detect if each finger is up based on a pre-determined relative distance from different points on the user's palm(to account for how far away the person is from the camera)
    if abs(lms.landmark[mp_hands.HandLandmark.THUMB_TIP].x - lms.landmark[mp_hands.HandLandmark.PINKY_MCP].x) <= distance_thresholds['thumb']*n:
        # assess x values for the thumb instead of y values because the thumb moves left and right instead of up and down
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
    
    cap = cv.VideoCapture(0)

    SAMPLES_COUNT = 0 # keep track of how many samples have been read
    MIN_SAMPLES = 3 # get 3 samples to detect a single digit
    input_samples = []

    distance_thresholds = {'thumb': 1.2, 'index': 2, 'middle': 2, 'ring': 2, 'pinky': 2}
    # coefficient that will help determine if a finger is up or not

    password_digit = None

    while SAMPLES_COUNT <= MIN_SAMPLES:

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = hands.process(frame) # get the processed frames results (i.e. normalized locations of critical points on each finger (like index finger tip) relative to the capture camera screen)

        if res.multi_hand_landmarks:
            # if a hand has been detected
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


# similar to get_finger_count but keeps track of time and exits if it doesn't detect a hand gesture after a certain time period
# refer to get_finger_count for further comments
def get_finger_count_with_time_restriction(mp_hands, mp_draw, hands, countdown = 5):
    cap = cv.VideoCapture(0)

    SAMPLES_COUNT = 0
    MIN_SAMPLES = 3
    input_samples = []

    distance_thresholds = {'thumb': 1.2, 'index': 2, 'middle': 2, 'ring': 2, 'pinky': 2}
    # coefficient that will help determine if a finger is up or not

    password_digit = None

    start = time.time()

    # exit the while loop if countdown has passed
    while SAMPLES_COUNT <= MIN_SAMPLES and time.time() - start < countdown:

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


if __name__ == "__main__":
    import mediapipe as mp

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

    while True:
        print(get_finger_count(mp_hands, mp_draw, hands))