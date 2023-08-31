import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMenu, QAction, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QFont, QCursor
from datetime import datetime
import pytz

class WorldClockWidget:
    def __init__(self, timezone='Asia/Shanghai', label_name='CHINA'):
        self.timezone = timezone
        self.label_name = label_name
        self.app = QApplication(sys.argv)
        self.window = self.DraggableWindow(timezone, label_name)
        self.window.label.setStyleSheet("color: white;")
        font = QFont("Comic Sans MS", 20)
        self.window.label.setFont(font)

        layout = QVBoxLayout(self.window)
        self.window.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.window.label)
        self.window.move(QCursor.pos())
    
    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    class DraggableWindow(QWidget):
        def __init__(self,timezone, label_name):
            super().__init__()
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.label = QLabel("Hello, World!", self)
            self.timezone = timezone
            self.label_name = label_name
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
            tz = pytz.timezone(self.timezone)
            current_time = datetime.now(tz).strftime('%H:%M:%S')
            self.label.setText(f"{self.label_name}        {current_time}")


# To use the widget
if __name__ == "__main__":
    widget = WorldClockWidget()  # Change timezone and label name as needed
    widget.run()
