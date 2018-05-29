import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random
from time import sleep

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import MMOSwarm as pso


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.m = PaintWidget(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(0, 0)
        button.clicked.connect(self.on_click)


        self.m.move(0, 0)
        self.m.resize(self.width, self.height)

        self.show()

    @pyqtSlot()
    def on_click(self):
        #print('PyQt5 button click')
        self.m.repaint()


class PaintWidget(QWidget):
    def __init__(self, QWidget):
        super(PaintWidget, self).__init__()
        self.pso = pso.MMOpso()
        self.pso.populate()
        print("fdf")

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.black)
        qp.setBrush(Qt.red)
        size = self.size()
        print("dcysfd")

        #players = self.pso.get_players()
        #self.pso.next_iteration()

        #for player in players:
        #    x = player.current['x'] * size.width()
        #    y = player.current['y'] * size.height()
        #    qp.drawEllipse(x, y, 5, 5)

        for i in range(1024):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            #qp.drawPoint(x, y)
            qp.drawEllipse(x, y, 5, 5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())