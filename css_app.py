label_camera_style = """
QLabel {
  font-size: 22px;
  padding: 12px 16px;
  border-radius: 8px;
  background-color: #e8e8e8;
  border: 5px solid #7133E6;
  color: #fff;
}
"""
label_result_style = """
QLabel {
  font-size: 16px;
  color: #e8e8e8;
  font-weight: bold;
  padding: 6px 12px;
  background-color: #100720;
  border: 2px solid #E926E0;
  border-radius: 5px;
}
"""
Text_result_style = """
QLineEdit {
  font-size: 16px;
  color: #000000;
  font-weight: bold;
  padding: 6px 12px;
  background-color: #D5C7EF;
  border: 2px solid #7133E6;
  border-radius: 10px;
}
"""

buttom_on_off_style = """
QPushButton {
  width: 165px;
  height: 62px;
  color: #fff;
  font-size: 17px;
  border-radius: 12px;
  background-color: #100720;
  border: none;
  border: 3px solid #E926E0;
}

QPushButton:pressed {
  background-color: #ff5ef7;
  transform: scale(0.9);
}
"""
buttom_clear_style = """
QPushButton {
  font-size: 10px;
  font-weight: bold;
  color: #FCFCFC;
  background-color: #100720;
  padding: 12px 24px;
  border-radius: 30px;
  border: 3px solid #7133E6;
}

QPushButton:pressed {
  background-color: #E926E0;
  border: 3px solid #E926E0;
  transform: translateY(4px);
}
"""

main_window = """
QWidget {
    background:qlineargradient(
        spread:pad,
        x1:0,y1:0,
        x2:1,y2:0,
        stop: 0 #A85CFF,
        stop: 0.5 #ED61E6,
        stop: 1 #2B2828
    );
    
}
"""