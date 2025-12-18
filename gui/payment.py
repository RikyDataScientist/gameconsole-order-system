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
        main_layout.setContentsMargins(20, 20, 20, 30)

        left_bar = QFrame()
        left_bar.setObjectName("sidebar")
        left_bar.setFixedWidth(220)

        left_layout = QVBoxLayout(left_bar)
        left_layout.setContentsMargins(30, 40, 30, 40)
        left_layout.setSpacing(5)

        title_left = QLabel("To Pay")
        title_left.setObjectName("title_left")
        title_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.price = QLabel()
        self.price.setObjectName("price")
        self.price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cancel_button = QPushButton("Cancel Payment")
        cancel_button.setObjectName("button")
        cancel_button.clicked.connect(self.cancel_payment)

        left_layout.addStretch()
        left_layout.addWidget(title_left)
        left_layout.addWidget(self.price)
        left_layout.addStretch()
        left_layout.addWidget(cancel_button)

        right_bar = QFrame()
        right_layout = QVBoxLayout(right_bar)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(40, 15, 40, 15)

        title = QLabel("Payment")
        title.setObjectName("title")

        frame = QFrame()
        frame.setObjectName("card")

        layout = QGridLayout(frame)
        layout.setVerticalSpacing(12)

        text = QLabel("Booking Id:")
        text.setObjectName("text")
        self.booking_id = QLabel()
        self.booking_id.setObjectName("text")
        layout.addWidget(text, 0, 0)
        layout.addWidget(self.booking_id, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        text1 = QLabel("Username:")
        text1.setObjectName("text")
        self.username = QLabel()
        self.username.setObjectName("text")
        layout.addWidget(text1, 1, 0)
        layout.addWidget(self.username, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        text2 = QLabel("Total Waktu Booking:")
        text2.setObjectName("text")
        self.time_booked = QLabel()
        self.time_booked.setObjectName("text")
        layout.addWidget(text2, 2, 0)
        layout.addWidget(self.time_booked, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)

        text3 = QLabel("Console:")
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

        main_layout.addWidget(left_bar)
        main_layout.addWidget(right_bar)

    def cancel_payment(self):
        self.stack.setCurrentIndex(0)
        self.input.clear()

    def update_info(self, controller):
        self.controller = controller
        if controller is None:
            self.price.setText("Rp0")
            self.booking_id.setText("-")
            self.username.setText("-")
            self.time_booked.setText("-")
            self.console.setText("-")
        else:
            self.price.setText(f"Rp{controller.booking.price}")
            self.booking_id.setText(str(controller.booking.booking_id))
            self.username.setText(controller.booking.username)
            self.time_booked.setText(
                f"{len(controller.booking.times)} Jam"
            )
            self.console.setText(controller.booking.console)

    def Pay(self):
        amount = self.input.text().strip()

        if amount == "":
            show_error("Input tidak boleh kosong")
            return

        if not amount.isdigit():
            show_error("Input hanya boleh angka")
            return

        amount = int(amount)
        try:
            msg = self.controller.pay(amount)
            show_info(msg)
            self.input.clear()
            self.stack.parent().data_booking = None
            self.stack.setCurrentIndex(0)
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
            background-color: #0d1117;
            border: 1px solid #58a6ff;
            border-radius: 16px;
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
