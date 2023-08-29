import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMenu, QAction, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRectF, QTimer, QTime
from PyQt5.QtGui import QPainterPath, QFont, QRegion, QCursor
from datetime import datetime
import pytz

class DraggableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label = QLabel("Hello, World!", self)
        # Rounded corners
        radius = 40.0
        path = QPainterPath()
        self.resize(500, 220)
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.move(QCursor.pos())

        # Initialize variables for mouse tracking
        self.dragging = False
        self.offset = QPoint()

        # Timer for long press detection
        self.long_press_timer = QTimer(self)
        self.long_press_timer.setInterval(1000)
        self.long_press_timer.timeout.connect(self.pin_to_top)
        self.long_pressed = False

        # Timer to update current time
        self.time_update_timer = QTimer(self)
        self.time_update_timer.setInterval(1000)
        self.time_update_timer.timeout.connect(self.update_time)
        self.time_update_timer.start()

        # Initial time update
        self.update_time()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            self.long_press_timer.start()
        elif event.button() == Qt.RightButton:
            menu = QMenu(self)
            close_action = QAction("Close Window", self)
            close_action.triggered.connect(self.close)
            menu.addAction(close_action)
            menu.exec_(event.globalPos())

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.long_press_timer.stop()

    def pin_to_top(self):
        self.long_press_timer.stop()
        self.long_pressed = True
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.show()

    def update_time(self):
        china_tz = pytz.timezone('Asia/Shanghai')
        china_time = datetime.now(china_tz).strftime('%H:%M:%S')
        self.label.setText("CHINA        " + china_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DraggableWindow()
    window.label.setStyleSheet("color: white;")
    font = QFont("Comic Sans MS", 20)
    window.label.setFont(font)

    layout = QVBoxLayout(window)
    window.label.setAlignment(Qt.AlignCenter)
    layout.addWidget(window.label)
    window.move(QCursor.pos())
    window.show()
    sys.exit(app.exec_())
