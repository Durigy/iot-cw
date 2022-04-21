from verify_password import check_password, setup_password
from lcd import setText
from buzzer import buzzer
# from button import read_button
import mediapipe as mp
import time
from ultra_sonic import person_detected
import threading as t
# from vision import get_finger_count
# from light import sort_light

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

unlocked = False
countdown_over = False
stop_countdown_for_disarmed = False

def start_countdown_for_alarm(countdown):
    global unlocked
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
    buzzer('--')
    setText('ARMED', 'green')
    time.sleep(1.5)
    setText('', 'off')

    global unlocked

    unlocked = False

    while True:
        if person_detected():
            countdown = 3
            unlocked = False
            thread = t.Thread(target=start_countdown_for_alarm, args=[countdown])
            thread.start()
            while True:
                if check_password(mp_hands, mp_draw, hands):
                    break
            break

    # at this point the password will have been accepted
    
    disarmed_mode()

def start_countdown_for_disarmed(countdown):
    global countdown_over, stop_countdown_for_disarmed
    start = time.time()
    while time.time() - start < countdown and not stop_countdown_for_disarmed:
        continue
    
    if stop_countdown_for_disarmed:
        stop_countdown_for_disarmed = False
        exit()

    countdown_over = True
    exit()

def disarmed_mode():
    global unlocked, countdown_over, stop_countdown_for_disarmed
    unlocked = True
    setText('', 'off')
    countdown = 5
    while True:
        if person_detected():
            countdown_over = False
            setText("5: Armed Mode")
            thread = t.Thread(target=start_countdown_for_disarmed, args=[countdown])
            thread.start()
            while not countdown_over:
                if get_finger_count(mp_hands, mp_draw, hands) == 5:
                    stop_countdown_for_disarmed = True
                    thread.join()
                    break
            if countdown_over:
                setText('', 'off')
                continue
            else:
                break

    armed_mode()

def set_off_alarm():
    # set off alarm and continuously check global unlock variable to turn it off
    while True:
        global unlocked
        if not unlocked:
            buzzer('-----')
        else:
            break
        time.sleep(1)
    disarmed_mode()


# for testing use password as a global variable
password = ''
def main():

    setText('', 'white')

    setup_password(mp_hands, mp_draw, hands)

    # disarmed_mode()

    armed_mode()



    # if person_detected():
    #     print('hello world')
    #     sort_light()
    #     setText('Enter your\nPassword')
    #     working_pwd = get_password(mp_hands, mp_draw, hands, pass_count=4)
    #     setText(f'[ACCESS GRANTED]\n{str(working_pwd)}', 'green')



main()