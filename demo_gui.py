import random
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from ASR.STT import read_from_microphone
from DialogManagement import *
from GUI.gui_utils import *
from IDSF.inference_module import JointBertTools
from Tasks import music, weather
from Tasks.utils import *

schema_path = './IDSF/schema.json'


class Pipeline:
    def __init__(self) -> None:
        self.model_dir = "IDSF/backup/sgd"
        self.batch_size = 32
        self.model = JointBertTools(model_dir=self.model_dir, batch_size=self.batch_size)

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = APP(self.MainWindow, model=self.model)

    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.start()
