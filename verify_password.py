import vision
from lcd import setText

def get_password(mp_hands, mp_draw, hands, pass_count=4):
    pwd_list = []
    finger_count = 0
    while len(pwd_list) != pass_count:
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

        setText(str(pwd_list))

    return pwd_list


def set_password(mp_hands, mp_draw, hands):
    pwd_list = []
    finger_count = 0
    while True:
        finger_count = vision.get_finger_count(mp_hands, mp_draw, hands)
        if finger_count == 0:
            break
        
        if len(pwd_list) == 0: pwd_list.append(finger_count)
        elif finger_count != pwd_list[-1]: pwd_list.append(finger_count)

        print(pwd_list)
        setText(pwd_list, 'white')

    return pwd_list




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
