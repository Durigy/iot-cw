from distutils.log import error
import time
import vision
from buzzer import buzzer
from lcd import setText
import bcrypt
# from ast import literal_eval # https://www.askpython.com/python/string/python-convert-string-to-list

def check_password(mp_hands, mp_draw, hands):
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

    while len(pwd_list) != len(list(hashed_pwd)):
        finger_count = vision.get_finger_count(mp_hands, mp_draw, hands)

        if finger_count == 0:
            pwd_list = []
            setText('Empty', 'red')
            continue

        if len(pwd_list) == 0:
            pwd_list.append(finger_count)
        elif finger_count != pwd_list[-1]:
            pwd_list.append(finger_count)

        print(pwd_list)

        setText(' '.join(str(i) for i in pwd_list))

    if bcrypt.checkpw(str(''.join(str(i) for i in pwd_list)), hashed_pwd):
        return True
    else:
        return False


def set_password(mp_hands, mp_draw, hands):
    pwd_list = []
    finger_count = 0
    while True:
        finger_count = vision.get_finger_count(mp_hands, mp_draw, hands)
        if finger_count == 0:
            buzzer('--')
            break
        
        if len(pwd_list) == 0:
            pwd_list.append(finger_count)
            buzzer('.')
        elif finger_count != pwd_list[-1]:
            pwd_list.append(finger_count)
            buzzer('.')

        print(pwd_list)
        setText(' '.join(str(i) for i in pwd_list), 'white')

    return pwd_list


def setup_password(mp_hands, mp_draw, hands):
    for _ in range(3):
        setText('', 'purple')
        buzzer('...')
        setText('CREATE PASSWORD', 'purple')
        time.sleep(0.5)
        
    while True:
        working_pwd = set_password(mp_hands, mp_draw, hands)
        if len(working_pwd) > 0:
            hashed_password = bcrypt.hashpw(str.encode(''.join(str(i) for i in working_pwd)), bcrypt.gensalt()).decode('utf-8')
            setText('PASSWORD CREATED', 'green')
            with open('p.txt', 'w') as f:
                f.write(hashed_password)
            break
        
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
