def identifyPassword(fingercount):
    global password_stack, input_samples

    # collect input samples (for error correction)
    if len(input_samples) < 4:
        input_samples.append(fingercount)
        return
        
    # next_digit will be determined based on input_samples
    next_digit = 0

    next_digit = Counter(input_samples).most_common(1)[0][0]
    print(next_digit)

    input_samples = []

    if next_digit == 0:
        password_stack = []
    else:
        if len(password_stack) != 0:
            if next_digit != password_stack[-1]:
                password_stack.append(next_digit)
        else:
            password_stack.append(next_digit)
            
    print(password_stack)

    if len(password_stack) == len(password):
        if password == password_stack:
            # print('unlocked')
            # password_stack = []
            # time.sleep(3)
            return password_stack
main