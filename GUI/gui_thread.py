import os

import numpy as np
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
