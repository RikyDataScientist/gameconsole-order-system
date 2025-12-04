from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from gui.room_menu import RoomGui
from gui.payment import PaymentGui
from controller.pay_controller import PayController
from utils.info_helper import show_error
import sys

class MainMenu(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setFixedSize(650, 430)

        layout = QVBoxLayout(self)
        self.stack = QStackedWidget()

        self.stack.addWidget(HomePage(self.user, self.stack))
        self.stack.addWidget(RoomGui(self.user, self.stack))

        layout.addWidget(self.stack)
        self.stack.setCurrentIndex(0)

class HomePage(QWidget):
    def __init__(self, user_log, stack):
        super().__init__()
        self.user = user_log
        self.stack = stack
        self.setFixedSize(650, 430)
        self.setStyleSheet(self.style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(30)

        title = QLabel("Welcome " + str(self.user.username))
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_frame = QFrame()
        btn_frame.setObjectName("card")
        btn_frame.setFixedWidth(300)

        btn_layout = QVBoxLayout(btn_frame)
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(20)

        subtitle = QLabel("Select Option")
        subtitle.setObjectName("text")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        order_btn = QPushButton("Book")
        order_btn.setObjectName("button")
        order_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        pay_btn = QPushButton("Pay")
        pay_btn.setObjectName("button")
        pay_btn.clicked.connect(self.execute_payment_page)

        btn_layout.addWidget(subtitle)
        btn_layout.addStretch()
        btn_layout.addWidget(order_btn)
        btn_layout.addWidget(pay_btn)

        layout.addWidget(btn_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(sys.exit)
        exit_btn.setObjectName("button")
        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignLeft)


    def payment_page(self):
        pass
        # controller = PayController(self.user)
        # if not controller.booking:
        #     raise ValueError("Tidak ada bookingan yang ditemukan untuk dibayar")

        # payment_gui = PaymentGui(self.stack, controller)
        # return payment_gui

    def execute_room_page(self):
        room_gui = RoomGui(self.user)
        self.stack.setCurrentIndex(3)
    def execute_payment_page(self):
        try:
            self.stack.setCurrentIndex(2)
        except ValueError as e:
            show_error(str(e))

    def style(self):
        return """
        QWidget {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI';
        }

        #card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 25px;
        }

        #title {
            font-size: 26px;
            font-weight: bold;
            color: #58a6ff;
        }

        #text {
            font-size: 20px;
            font-weight: bold;
            color: #58a6ff;
            background: transparent;
        }

        #button {
            background-color: #238636;
            color: white;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
        }
        #button:hover {
            background-color: #2ea043;
        }
        #button:pressed {
            background-color: #196c2e;
        }
        """
