from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        for i in range(101):
            self.update_progress.emit(i)
            self.msleep(50)


class Installer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_installation)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(start_button)
        self.setLayout(layout)

        self.setWindowTitle("Installer")
        self.show()

    def start_installation(self):
        worker = WorkerThread(self)
        worker.update_progress.connect(self.update_progress)
        worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
