from datetime import datetime
from distutils.log import error
import pwd
import time
import vision
from buzzer import buzzer
from lcd import setText
import bcrypt
from os.path import exists
import requests
# from main import api_key, url, unlocked, device_name, device_id
# from ast import literal_eval # https://www.askpython.com/python/string/python-convert-string-to-list

# api_key = '851db27bf1b1c6a0dc8f' #ae2ce6622d27d55654d784614e77'
# url = 'https://5qu.me/api/'
# device_name = "Security System 1"
# device_id = ''
# unlocked = False

# function to check if the password is correct
def check_password(mp_hands, mp_draw, hands, url, api_key, device_id):

    setText('', 'white')
    
    reset_counter = 0

    pwd_list = []
    finger_count = 0

    hashed_pwd = ''

    try:
        f = open("p.txt", 'r')
        hashed_pwd = f.read()
        f.close()
    except:
        print('Error reading password!')
        return

    try:
        # check if password has been updated online
        setText('Checking\nPassword', 'blue')

        r = requests.post(
            url+'device/get', 
            data={
                'api_key': api_key, 
                'device_id': device_id
            }
        )
        
        time.sleep(1)

        updated_hashed_password = r.json()['hashed_password']
        # print(r.json())
        # print(updated_hashed_password)
        # print(hashed_pwd)

        # if password received from server is not the same as the same password, this means that the password has been updated from the online interface
        if updated_hashed_password != hashed_pwd:
            setText('[Password Updated]')
            time.sleep(1)
            with open('p.txt', 'w') as f:
                f.write(updated_hashed_password)
            hashed_pwd = updated_hashed_password
        else:
            pass        
    except:
        pass

    setText('[Enter\nPassword]', 'white')

    # the inputted password through computer vision is hashed and checked in each loop to see if it matches the correct password
    while not bcrypt.checkpw(str.encode(''.join(str(i) for i in pwd_list)), str.encode(hashed_pwd)):
        try:
            finger_count = vision.get_finger_count(mp_hands, mp_draw, hands) # finger count is password digit

            if finger_count == 0:
                # fist is detected, this means reset password
                pwd_list = []
                setText('Empty', 'red')
                # finger_count += 1
                reset_counter += 1
                continue

            if len(pwd_list) == 0:
                pwd_list.append(finger_count)
            elif finger_count != pwd_list[-1]:
                # only read password digits list if the detected digit is not the same as the last inputted digit (this means we can't have 1225 as a password for instance)
                pwd_list.append(finger_count)

            print(pwd_list)
            print(' '.join(str(i) for i in pwd_list))
            to_display = ' '.join(str(i) for i in pwd_list) # parsing a string of the current inputted password to be displayed in the LCD display
            setText(to_display)
            buzzer('.')
        except:
            print('check_password_error in iteration')

    # if bcrypt.checkpw(str(''.join(str(i) for i in pwd_list)), hashed_pwd):
    # print('returning true check_password')

    try:
        # send how many times the user had to reset the inputted password - this will determine how accurate is the computer vision software
        requests.post(url+'device/send_data', data={
            'reset_counter': reset_counter, 
            'api_key': api_key, 
            'device_id': device_id
        })
    except:
        pass

    return True
    # else:
    #     return False


def set_password(mp_hands, mp_draw, hands):
    pwd_list = []
    finger_count = 0
    # loops until the a fist is recognised
    while True:
        finger_count = vision.get_finger_count(mp_hands, mp_draw, hands)
        # if a fist is make the while loop is broken and password is returned
        if finger_count == 0:
            # fist detected - ask user 
            buzzer('--')
            break
        
        # adds the the finger number to the password stack
        if len(pwd_list) == 0:
            pwd_list.append(finger_count)
            buzzer('.')
        elif finger_count != pwd_list[-1]:
            pwd_list.append(finger_count)
            buzzer('.')

        print(pwd_list)
        setText(' '.join(str(i) for i in pwd_list), 'white') # sets the text of the lcd

    return pwd_list


# function to set up the password
def setup_password(mp_hands, mp_draw, hands, url, api_key, device_name, unlocked):

    reset_counter = 0

    # checks if the file exists then if there is a password already stored it brakes out of the setup function
    if exists('p.txt'):
        try:
            f = open("p.txt", 'r')
            hashed_pwd = f.read()
            f.close()
            if hashed_pwd != '': return (False, '')
        except:
            print('Error reading password!')
            return (False, '')

    # lcd setup stuff
    for _ in range(1):
        setText('', 'purple')
        buzzer('...')
        setText('CREATE PASSWORD', 'purple')
        time.sleep(0.5)

    # loops until a the password is setup and confirmed by the user
    while True:
        working_pwd = set_password(mp_hands, mp_draw, hands)

        setText('Save password?\n1: Yes, 2: No')

        decision = ''

        # loops until the user decides to confirm the password or enter
        while True:
            decision = vision.get_finger_count(mp_hands, mp_draw, hands)

            if decision not in (1, 2):
                continue

            break
        
        # if the password is entered and confirmed then it is encrypted
        if len(working_pwd) > 0 and decision == 1:
            buzzer('.')
            hashed_password = bcrypt.hashpw(str.encode(''.join(str(i) for i in working_pwd)), bcrypt.gensalt()).decode('utf-8')
            setText('PASSWORD CREATED', 'green')
            time.sleep(2)
            # writes the hashed password to the file
            with open('p.txt', 'w') as f:
                f.write(hashed_password)


            device_id = ''
            try:
                # sends the device setup info to the api
                r = requests.post(
                    url+'device', 
                    data = {
                        'hashed_password': hashed_password,
                        'api_key':api_key,
                        'name': device_name,
                        'is_armed': not unlocked
                    }
                )

                # gets the generated device id returned from the api
                device_id = r.json()['id']

                # writes the device id to a file
                with open('device_id.txt', 'w') as f:
                    f.write(device_id)

            except:
                pass

            # print(r.text)


            # device_id = r.json()
            # print(device_id)
            print(device_id)

            time.sleep(2)

            # gets the current utc time
            dt = datetime.utcnow()

            print(dt)

            try:
                # post device info to the api
                a = requests.post(
                    url+'device/send_data', 
                    data={
                        'reset_counter': str(reset_counter), 
                        'api_key': api_key, 
                        'device_id': device_id,
                        'time': str(dt),
                        'is_intruder': None,
                        'light': None
                        # 'is_intruder': '',
                        # 'light': '' #send FALSE values using empty strings
                    }
                )
                print(a.json())
                print(f'reset counter: {reset_counter}')
                
            except:
                pass


            # new = requests.post(url+'device/get', data={'api_key':api_key, 'device_id':device_id})
            # print(new.json())


            # returns the device id
            return (True, device_id)
            # break
        else:
            reset_counter += 1
            setText('CREATE PASSWORD', 'purple')
            buzzer('..')
            time.sleep(2)
        
    return True



### old stuff ###


# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

# cap = cv.VideoCapture(0)

# password = [2, 5, 4]
# password_stack = []
# input_samples = []

# def get_password(pass_count=4):
#     pwd_list = []
#     while not len(pwd_list) == pass_count:
#         pwd_list.append()
#     return pwd_list

# def setUpPassword():
#     pass

# def get_password(pass_count=4):
#     pwd_list = []
#     while not len(pwd_list) == pass_count:
#         pwd_list.append()

#         # collect input samples (for error correction)
#         if len(input_samples) < 4:
#             input_samples.append(fingercount)
#             return
            
#         # next_digit will be determined based on input_samples
#         next_digit = 0

#         next_digit = Counter(input_samples).most_common(1)[0][0]
#         print(next_digit)

#         input_samples = []

#         if next_digit == 0:
#             password_stack = []
#         else:
#             if len(password_stack) != 0:
#                 if next_digit != password_stack[-1]:
#                     password_stack.append(next_digit)
#             else:
#                 password_stack.append(next_digit)
                
#         print(password_stack)
#         return password_stack
#     return pwd_list



# def identifyPassword(fingercount):
#     global password_stack, input_samples

#     # collect input samples (for error correction)
#     if len(input_samples) < 4:
#         input_samples.append(fingercount)
#         return
        
#     # next_digit will be determined based on input_samples
#     next_digit = 0

#     next_digit = Counter(input_samples).most_common(1)[0][0]
#     print(next_digit)

#     input_samples = []

#     if next_digit == 0:
#         password_stack = []
#     else:
#         if len(password_stack) != 0:
#             if next_digit != password_stack[-1]:
#                 password_stack.append(next_digit)
#         else:
#             password_stack.append(next_digit)
            
#     print(password_stack)
#     return password_stack

    # if len(password_stack) == len(password):
    #     if password == password_stack:
    #         # print('unlocked')
    #         # password_stack = []
    #         # time.sleep(3)
    #         return password_stack
