from verify_password import get_password
from verify_password import get_password, set_password
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)


def main():
    # while True:
    #     vision.get_finger_count(mp_hands, mp_draw, hands)

    get_password(mp_hands, mp_draw, hands, pass_count=4)

main()