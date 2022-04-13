from verify_password import get_password
from verify_password import get_password, set_password
from lcd import setText
import mediapipe as mp
import time
# from ultra_sonic import person_detected
# from light import sort_light

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

def read_password():
    try:
        f = open("p.txt", 'r')
        p = f.read()
        f.close()
        return p
    except:
        return ''

def setup_password():
    setText('CREATE PASSWORD', 'purple')
    time.sleep(1.5)
    setText('', 'purple')
    time.sleep(1)
    setText('CREATE PASSWORD', 'purple')
    time.sleep(1.5)
    setText('', 'purple')
    time.sleep(1)
    setText('CREATE PASSWORD', 'purple')

    working_pwd = set_password(mp_hands, mp_draw, hands)

    setText('PASSWORD CREATED', 'green')
    with open('p.txt', 'w') as f:
        f.write(str(working_pwd))

    return working_pwd

def main():

    password = read_password()
    setText('')

    if len(password) == 0:
        password = setup_password()

        



    # if person_detected():
    #     sort_light()
    #     setText('Enter your\nPassword')
    #     working_pwd = get_password(mp_hands, mp_draw, hands, pass_count=4)
    #     setText(f'[ACCESS GRANTED]\n{str(working_pwd)}', 'green')



main()