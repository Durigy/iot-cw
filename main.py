from verify_password import check_password, set_password
from lcd import setText
from buzzer import buzzer
# from button import read_button
import mediapipe as mp
import time
from ultra_sonic import person_detected
import threading as t
# from light import sort_light

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

unlocked = False
countdown_over = False

def read_password():
    try:
        f = open("p.txt", 'r')
        p = f.read()
        f.close()
        return p
    except:
        return ''

def setup_password():
    setText('', 'purple')
    buzzer('...')
    setText('CREATE PASSWORD', 'purple')
    time.sleep(1)
    setText('', 'purple')
    time.sleep(0.5)
    setText('CREATE PASSWORD', 'purple')
    time.sleep(1)
    setText('', 'purple')
    time.sleep(0.5)
    setText('CREATE PASSWORD', 'purple')

    working_pwd = set_password(mp_hands, mp_draw, hands)

    setText('PASSWORD CREATED', 'green')
    with open('p.txt', 'w') as f:
        f.write(str(working_pwd))

    return working_pwd

def start_countdown(countdown):
    global unlocked, countdown_over
    start = time.time()
    while time.time() - start < countdown and not unlocked:
        continue
    if unlocked:
        exit()
        # return
    else:
        # prioritize setting off the alarm then return to the caller
        set_off_alarm()
        exit()


def armed_mode():
    setText('', 'off')
    while True:
        if person_detected():
            global unlocked, countdown_over
            countdown = 30
            unlocked = False
            countdown_over = False
            thread = t.Thread(target=start_countdown, args=[countdown])
            thread.start()
            while not unlocked:
                if check_password(mp_hands, mp_draw, hands):
                    unlocked = True
            break

    # at this point the password will have been accepted
    unlocked = False
    countdown_over = False
    disarmed_mode()


def disarmed_mode():
    setText('', 'off')            

def set_off_alarm():
    # set off alarm and continuously check global unlock variable to turn it off
    global unlocked
    while not unlocked:
        buzzer('-----')
        time.sleep(1)
    disarmed_mode()


# for testing use password as a global variable
password = ''
def main():

    setText('', 'white')

    password = read_password()

    if len(password) == 0:
        password = setup_password()
        time.sleep(3)
        setText('', 'white')

    disarmed_mode()

    # FOR TESTING WE CALL armed()
    armed_mode()



    # if person_detected():
    #     sort_light()
    #     setText('Enter your\nPassword')
    #     working_pwd = get_password(mp_hands, mp_draw, hands, pass_count=4)
    #     setText(f'[ACCESS GRANTED]\n{str(working_pwd)}', 'green')



main()