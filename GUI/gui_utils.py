import os
import sys
from pathlib import Path

import pandas as pd
from numpy.lib.function_base import extract
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QMessageBox, QTableWidgetItem,
                             QVBoxLayout, QWidget)
from requests.models import encode_multipart_formdata

try:
    from DialogManagement import *
    from Tasks import music, weather
    from Tasks.utils import *

    from GUI.chatbot_gui import *
except Exception as e:
    sys.stdout.write(str(e))
    from chatbot_gui import *


class APP(Ui_MainWindow, QWidget):
    def __init__(self, MainWindow, model=None) -> None:
        super().__init__()
        # self.MainWindow = MainWindow
        self.setupUi(MainWindow=MainWindow)
        self.idsf_model = model

        self.StopButton.clicked.connect(self.stop_program)
        self.InputMessage.returnPressed.connect(self.pipeline)
        self.dialog_state_tracking = [{"dialog_id": 0,
                                       "begin_time": 0,
                                       "end_time": 0,
                                       "turns": [{"speaker": "Bot",
                                                 "utterance": "hello there",
                                                  "domain": "",
                                                  "intent": "",
                                                  "slots": []
                                                  },
                                                 ]
                                       }]
        self.temp_dialog_state_tracking = []
        self.current_text = ''

    # =================================control flow=================================

    def stop_program(self):
        print('-> From: stop_program')
        sys.exit(1)
        pass

    def popup_msg(self, msg, src_msg='', type_msg='error'):
        """Create popup window to the ui

        Args:
            msg (str): message you want to show to the popup window
            src_msg (str, optional): source of the message. Defaults to ''.
            type_msg (str, optional): type of popup. Available: warning, error, information. Defaults to 'error'.
        """
        try:
            self.popup = QMessageBox()
            if type_msg.lower() == 'warning':
                self.popup.setIcon(QMessageBox.Warning)
                self.is_error = True
            elif type_msg.lower() == 'error':
                self.popup.setIcon(QMessageBox.Critical)
                self.is_error = True
            elif type_msg.lower() == 'info':
                self.popup.setIcon(QMessageBox.Information)

            self.popup.setText(f"[{type_msg.upper()}] -> From: {src_msg}\nDetails: {msg}")
            self.popup.setStandardButtons(QMessageBox.Ok)
            self.popup.exec_()
            print(f'[{type_msg.upper()}]: {msg} from {src_msg}')
        except Exception as e:
            print('-> From: popup_msg', e)
    # ===============================dialogue control==========================

    def get_input_message(self):
        # *1* get the message from the input box
        text = self.InputMessage.text()
        return text if len(text) > 0 else ''
        # return text if len(text) > 0 else ''

    def display_message(self, speaker='User', message='', clear_display=False):
        if not clear_display:
            # *1* get current message from the dialog window
            print(f'[{speaker}]: {message}')
            widget = QWidget()                 # Widget that contains the collection of Vertical Box
            vbox = QVBoxLayout()
            # *2* add the message to the end
            self.temp_dialog_state_tracking.append(f"[{speaker}]: {message}")

            for msg in self.temp_dialog_state_tracking:
                object = QLabel(msg)
                vbox.addWidget(object) # create widget inside the scroll box
            widget.setLayout(vbox)

            # *3* scroll to the bottom
            self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWidget(widget)
            # self.MainWindow.setCentralWidget(self.scrollArea)
            # auto scroll to bottom
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
            # *4* update the message window
        else:
            self.scrollArea.close()
        pass

    # =================================pipeline=================================
    def pipeline(self):
        message = self.get_input_message()
        try:
            # *1* get the message from the input box
            if len(message) > 0:
                # *2* get the response from the model
                # print(self.idsf_model.predict([message]))

                extract_intent, utterance = self.idsf_model.predict([message])[-1].split('->')
                extract_slots = get_expression(utterance)
                # print(extract_intent, utterance, extract_slots)

                # *2.1* update the dialog state tracking
                self.dialog_state_tracking[-1]['turns'].append(
                                                        {"speaker": "User",
                                                         "utterance": message,
                                                         "domain": "",
                                                         "intent": extract_intent,
                                                         "slots": extract_slots})

                print(self.dialog_state_tracking)

                log_writer(r'log.txt', self.dialog_state_tracking)
                # *3.0* perform tasks

                # *3.1* display the response
                self.display_message(speaker='User', message=message)
                self.display_message(speaker='User', message=utterance)

                self.InputMessage.clear()

        except Exception as e:
            self.popup_msg(msg=str(e), src_msg='pipeline')
        pass


def log_writer(log_file, log_data):
    try:
        with open(log_file, 'a') as f:
            current_dialog = log_data[-1]
            dialog_id = current_dialog['dialog_id']
            begin_time = current_dialog['begin_time']
            end_time = current_dialog['end_time']
            spk = current_dialog['turns'][-1]['speaker']
            utterance = current_dialog['turns'][-1]['utterance']
            log_msg = f"{dialog_id} [{begin_time} - {end_time}] {spk}: {utterance}"
            f.write(log_msg + '\n')
    except Exception as e:
        print(e)


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = APP(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
    """
    pipeline
    ...
    get the time
    them thanh keo ngang
    cach viet GUI
    pyuic5 <filename>.ui > <filename>.py
    trinh bay he thong GUI: cac buoc lam tu qt -> python -> ... -> demo_gui.py
    """
