import os
import pickle
import mediapipe as mp
import cv2
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)

data = []
labels = []
sample_count = 0  
count_img =0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []
            x_ = []
            y_ = []

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
            cv2.imshow('Hand Tracking', frame)

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                for i in range(200):
                    data.append(data_aux)
                    print('\033[91m'+'data_aux: ' + '\033[92m', data_aux)
                    labels.append(count_img)  
                sample_count += 1
                if sample_count ==21:
                    count_img += 1
                    sample_count = 0
                print(f"Sample {sample_count} captured.")
                print(f"\n\n\n\n\n=============================== {count_img} =======================.")

            
            elif cv2.waitKey(1) & 0xFF == ord('z'):
                print("Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                break


with open('data_cam.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print(f"Data saved with {len(data)} samples.")