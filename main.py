import vision

def main():
    while True:
        print(vision.main())
    pass
    
def setUpPassword():
    print('Start by making a fist.')
    while True:

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = hands.process(frame)

        if res.multi_hand_landmarks:
            fingercount = detectFingersUp(res, frame)
            if fingercount == 0:
                pass
            

        cv.imshow('output', cv.cvtColor(frame, cv.COLOR_RGB2BGR))

        if cv.waitKey(1) == 'q':
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()