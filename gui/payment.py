from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QStackedWidget,
    QLabel,
    QFrame,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from utils.info_helper import show_error, show_info


class PaymentGui(QWidget):
    def __init__(self, stack, controller):
        super().__init__()
        self.stack = stack
        self.controller = controller
        self.setFixedSize(650, 430)
        self.setStyleSheet(self.style())

        main_layout = QHBoxLayout(self)

        sidebar = QFrame()
        sidebar.setStyleSheet("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(30, 40, 30, 40)
        sidebar_layout.setSpacing(5)

        title_left = QLabel("To Pay")
        title_left.setObjectName("title_left")
        title_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.price = QLabel()
        self.price.setObjectName("price")
        self.price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cancel_button = QPushButton("Cancel Payment")
        cancel_button.setObjectName("button")
        # button.clicked.connect(currentindex)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(title_left)
        sidebar_layout.addWidget(self.price)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(cancel_button)

        rightbar = QFrame()
        right_layout = QVBoxLayout(rightbar)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(40, 20, 40, 20)

        title = QLabel("Payment")
        title.setObjectName("title")

        frame = QFrame()
        frame.setObjectName("card")

        layout = QGridLayout(frame)
        layout.setVerticalSpacing(12)

        text = QLabel("Booking Id")
        text.setObjectName("text")
        self.booking_id = QLabel()
        self.booking_id.setObjectName("text")

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.booking_id, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        text1 = QLabel("Username")
        text1.setObjectName("text")
        self.username = QLabel()
        self.username.setObjectName("text")

        layout.addWidget(text1, 1, 0)
        layout.addWidget(self.username, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        text2 = QLabel("Console")
        text2.setObjectName("text")
        self.time_booked = QLabel()
        self.time_booked.setObjectName("text")

        layout.addWidget(text2, 2, 0)
        layout.addWidget(self.time_booked, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)

        text3 = QLabel("Console")
        text3.setObjectName("text")
        self.console = QLabel()
        self.console.setObjectName("text")

        layout.addWidget(text3, 3, 0)
        layout.addWidget(self.console, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.input = QLineEdit()
        self.input.setObjectName("inputtext")
        self.input.setPlaceholderText("Fill Your Money")

        button1 = QPushButton("Pay")
        button1.setObjectName("button")
        button1.clicked.connect(self.Pay)

        right_layout.addWidget(title)
        right_layout.addWidget(frame)
        right_layout.addWidget(self.input)
        right_layout.addWidget(button1, Qt.AlignmentFlag.AlignCenter)
        right_layout.addStretch()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(rightbar)

    def update_info(self, controller):
        self.controller = controller
        if controller is None:
            self.prices.setText("Rp0")
            self.booking_id.setText("-")
            self.username.setText("-")
            self.time_booked.setText("-")
            self.console.setText("-")
        else:
            self.price.setText(f"Rp{controller.booking.price}")
            self.booking_id.setText(str(controller.booking.booking_id))
            self.username.setText(controller.booking.username)
            self.time_booked.setText(
                ", ".join([f"{t}:00" for t in controller.booking.times])
            )
            self.console.setText(controller.booking.console)
        
    def Pay(self):
        amount = self.input.text().strip()

        if amount == "":
            show_error("Input tidak boleh kosong")
            return

        if not amount.isdigit():
            show_error("Input hanya boleh angka")

        amount = int(amount)
        try:
            msg = self.controller.pay(amount)
            show_info(msg)
            self.controller.save()
            # self.stack.currentindex(0)
        except Exception as e:
            show_error(str(e))

    def style(self):
        return """
        QWidget {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI';
        }
        #sidebar {
            background-color: #161b22;
            border-right: 1px solid #1f2937;
        }
        #price {
            font-size: 32px;
            font-weight: bold;
            color: #58a6ff;
            background: transparent;
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

        #title_left {
            font-size: 20px;
            font-weight: bold;
            color: #58a6ff;
            background: transparent;
        }

        #text {
            font-size: 13px;
            background: transparent;
            color: white;
        }

        #inputtext {
            background-color: #0d1117;
            border: 2px solid #30363d;
            padding: 12px;
            border-radius: 10px;
            font-size: 15px;
            margin-bottom: 18px;
            color: #c9d1d9;
        }
        #inputtext:focus {
            border: 2px solid #58a6ff;
            background-color: #0c162d;
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
