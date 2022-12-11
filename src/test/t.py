from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedLayout
import sys


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.hbox = QHBoxLayout()
        self.stack = QStackedLayout()
        self.init()

    def switch_to_r1(self):
        self.stack.setCurrentIndex(0)

    def switch_to_r2(self):
        self.stack.setCurrentIndex(1)

    def init_left_widget(self):
        vbox = QVBoxLayout()
        btn1 = QPushButton("按钮1")
        btn2 = QPushButton("按钮2")
        btn1.clicked.connect(self.switch_to_r1)
        btn2.clicked.connect(self.switch_to_r2)
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)

        self.hbox.addLayout(vbox)

    def init_right_widget1(self):
        label1 = QLabel("页面1")
        self.stack.addWidget(label1)

    def init_right_widget2(self):
        label2 = QLabel("页面2")
        self.stack.addWidget(label2)

    def init(self):
        self.init_left_widget()
        self.init_right_widget1()
        self.init_right_widget2()

        self.stack.setCurrentIndex(0)
        self.hbox.addLayout(self.stack)
        self.setLayout(self.hbox)

        self.setFixedSize(300, 150)
        self.setWindowTitle("测试")
        self.show()


app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec())

