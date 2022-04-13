import vision
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)


def main():
    while True:
        vision.get_finger_count(mp_hands, mp_draw, hands)


main()