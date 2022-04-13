from verify_password import get_password
from verify_password import get_password, set_password
from lcd import setText
import mediapipe as mp
from ultra_sonic import person_detected
from light import sort_light

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

working_pwd = []
pwd = []

def main():
    if len(pwd) == 0:
        setText('Setup your\nPassword')
        pwd = set_password(mp_hands, mp_draw, hands)
        setText('Setup your\nPassword')


    if person_detected():
        sort_light()
        setText('Enter your\nPassword')
        working_pwd = get_password(mp_hands, mp_draw, hands, pass_count=4)
        setText(f'[ACCESS GRANTED]\n{str(working_pwd)}', 'green')



main()