import cv2
import time

cap_left = cv2.VideoCapture(0)
cap_right = cv2.VideoCapture(1)

frame_data = []  # store timestamps + frame indices

start_time = time.time()
frame_idx = 0

try:
    while True:
        ret_l, frame_l = cap_left.read()
        ret_r, frame_r = cap_right.read()
        if not ret_l or not ret_r:
            continue

        t = time.time() - start_time
        frame_data.append((frame_idx, t))

        # Display frames in VNC
        cv2.imshow('Left', frame_l)
        cv2.imshow('Right', frame_r)

        frame_idx += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()
