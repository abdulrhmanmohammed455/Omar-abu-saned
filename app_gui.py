import sys
import cv2
import pickle
import numpy as np
import mediapipe as mp
import css_app
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

model_dict = pickle.load(open('./Models/model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
labels_dict = {0 : 'ا' ,1 : 'ب' ,2 : 'ث' ,3 : 'ت' ,4 : 'ج' ,
               5 : 'ح' ,6 : 'خ' ,7 : 'د' ,8 : 'ذ' ,9 : 'ر' ,
               10 : 'ز' ,11 : 'س' ,12 : 'ش' ,13 : 'ص' ,14 : 'ض' ,
               15 : 'ط' ,16 : 'ظ' ,17 : 'ع' ,18 : 'غ' ,19 : 'ف' ,
               20 : 'ق' ,21 : 'ك' ,22 : 'ل' ,23 : 'م' ,24 : 'ن' ,
               25 : 'ه' ,26 : 'و' ,27 : 'ي' ,28 : 'ة' ,29 : 'لا'}

cap = cv2.VideoCapture(0)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('تعرف على الإشارات')
window.setGeometry(100, 100, 1000, 700)
window.setStyleSheet(css_app.main_window)

camera_label = QLabel(window)
camera_label.setStyleSheet(css_app.label_camera_style)
camera_label.setFixedSize(980, 480)
camera_label.move(10, 30)

result_label = QLabel('النتيجة: ', window)
result_label.setStyleSheet(css_app.label_result_style)
result_label.move(840, 530)
result_label.resize(90, 60)

result_text = QLineEdit('', window)
result_text.setStyleSheet(css_app.Text_result_style)
result_text.move(190, 530)
result_text.resize(650, 60)

clear_button = QPushButton('مسح', window)
clear_button.setStyleSheet(css_app.buttom_clear_style)
clear_button.resize(80, 60)
clear_button.move(100, 530)

toggle_button = QPushButton('تشغيل الكاميرا', window)
toggle_button.setStyleSheet(css_app.buttom_on_off_style)
toggle_button.move(1, 630)
toggle_button.setCheckable(True)

timer = QTimer()

hand_timer = QTimer()



def update_frame():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        image = QImage(frame_rgb, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        scaled_image = image.scaled(camera_label.width(), camera_label.height(), QtCore.Qt.KeepAspectRatio)
        camera_label.setPixmap(QPixmap.fromImage(scaled_image))

def process_hand_signal():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            data_aux, x_, y_ = [], [], []
            H, W, _ = frame.shape

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))
            
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]
            add_letter(predicted_character)
        image = QImage(frame_rgb, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        scaled_image = image.scaled(camera_label.width(), camera_label.height(), QtCore.Qt.KeepAspectRatio)
        camera_label.setPixmap(QPixmap.fromImage(scaled_image))

def clear_label():
    result_text.setText('')

def add_letter(char_scann):
    text = result_text.text()
    if len(text) > 1:
        if text[-1] != str(char_scann):
            text += char_scann
            result_text.setText(text)
    else:
        text += char_scann
        result_text.setText(text)

def toggle_camera():
    if toggle_button.isChecked():
        toggle_button.setText('إيقاف الكاميرا')
        timer.start(20)  
        hand_timer.start(1000)  
    else:
        toggle_button.setText('تشغيل الكاميرا')
        timer.stop()
        hand_timer.stop()

clear_button.clicked.connect(clear_label)
toggle_button.clicked.connect(toggle_camera)

timer.timeout.connect(update_frame)

hand_timer.timeout.connect(process_hand_signal)

window.show()

def close_event(event):
    cap.release()
    cv2.destroyAllWindows()
    event.accept()

window.closeEvent = close_event

sys.exit(app.exec_())
