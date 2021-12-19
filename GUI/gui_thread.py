import os
import sys

import numpy as np
from ASR.STT import Recognizer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal


class Thread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, list)

    def __init__(self, model=None):
        super().__init__()
        self.run_flag = True
        # initmodel here
        self.model = model

    def run(self):
        while self.run_flag:
            pass

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.run_flag = False
        self.wait()


class VoiceThread(QThread):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = Recognizer()
        self.run_flag = True

    def run(self):
        text = self.recognizer.read_from_microphone()
        try:
            self.textChanged.emit(text)
            print("You said: {}".format(text))
        except Exception as e:
            print(e)
