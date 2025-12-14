import json
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from controller.booking_controller import BookingController
from datetime import time
from utils.info_helper import show_info, show_error


class BookingDialog(QDialog):
    def __init__(self, callback, user, room, selected_times):
        super().__init__()
        self.callback = callback
        self.book = BookingController(user=user, room=room)  # Sesuaikan dengan user dan room yang sebenarnya
        self.selected_times = selected_times
        self.setWindowTitle("Sistem Booking Console")

        self.resize(650, 430)

        font_besar = QFont("Arial", 14)
        self.setFont(font_besar)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title_label = QLabel(f"Booking {self.book.room.model.name_room}")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        frame = QFrame()

        h1 = QGridLayout(frame)
        h1.addWidget(QLabel("Pilih Waktu Mulai:"), 0, 0, 1, 5)

        self.buttons = []
        for row in range(1, 3):
            for col in range(5):
                waktu = f"{8 + (row - 1) * 5 + col}:00"
                self.btn = QPushButton(waktu)
                self.btn.setObjectName("button")
                self.btn.setCheckable(True)
                self.btn.setStyleSheet("""
            #button {
                background: #0d1117;
                border-radius: 13px;
                border: 2px solid #58a6ff
                }
            #button:hover {
                background-color: #2b7bff;
                border-color: #58a6ff;
                }
            #button:pressed {
                background-color: #165bb7;
                border-color: #3a8bff;
                }
            #button:checked {
                background-color: #1158d6;
                }
                """)
                self.btn.setFixedSize(100, 40)
                self.btn.clicked.connect(self.click_to_update)
                self.buttons.append(self.btn)
                h1.addWidget(self.btn, row, col)
        layout.addWidget(frame)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Pilih Console:"))

        self.combo_console = QComboBox()
        self.combo_console.setObjectName("box")
        self.combo_console.addItems(["PS5", "PS4", "Xbox Series X", "Nintendo Switch"])
        self.combo_console.setMinimumWidth(300)
        self.combo_console.currentIndexChanged.connect(self.update_price)
        h2.addWidget(self.combo_console)
        layout.addLayout(h2)

        h3 = QVBoxLayout()
        self.price_label = QLabel("Harga Total: Rp0")
        h3.addWidget(self.price_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(h3)

        self.btn_simpan = QPushButton("Simpan Booking")
        self.btn_simpan.setMinimumHeight(50)
        self.btn_simpan.setStyleSheet("font-size: 18px;")
        self.btn_simpan.clicked.connect(self.simpan_booking)
        layout.addWidget(self.btn_simpan)

        self.setLayout(layout)
        self.update_buttons()
        self.update_price()

    def click_to_update(self):
        self.update_price()

    def update_buttons(self):
        booked_times = self.book.room.model.booked_times
        if self.selected_times is None or self.selected_times == "All":
            preselected_hours = []
        else:
            preselected_hours = [self.selected_times]

        for btn in self.buttons:
            hour = time(int(btn.text().split(":")[0]))
            if hour in booked_times:
                btn.setEnabled(False)
                btn.setChecked(False)
                btn.setStyleSheet("""
            #button {
                background-color: #30363d;
                color: #8b949e;
                border: 1px solid #21262d;
                border-radius: 13px;
                }
                """)
                btn.setToolTip("Sudah dipesan")
            else:
                btn.setEnabled(True)
                if hour in preselected_hours:
                    btn.setChecked(True)
                else:
                    btn.setChecked(False)

    def update_price(self):
        selected_console = self.combo_console.currentText()
        selected_times = [time(int(btn.text().split(":")[0])) for btn in self.buttons if btn.isChecked() and btn.isEnabled()]

        if not selected_times:
            self.price_label.setText("Harga Total: Rp0")
            return

        total_price = self.book.price(selected_console, selected_times)
        self.price_label.setText(f"Harga Total: Rp{total_price}")

    def simpan_booking(self):
        selected_console = self.combo_console.currentText()
        selected_times = [time(int(btn.text().split(":")[0])) for btn in self.buttons if btn.isChecked() and btn.isEnabled()]

        if not selected_times:
            show_error("Silakan pilih minimal satu waktu booking.")
            return

        try:
            booking = self.book.create_booking(selected_console, selected_times)
            self.book.room.order(selected_times)
            show_info(f"Booking berhasil!\nID Booking: {booking.booking_id}\nTotal Harga: Rp{booking.price}")
            self.callback.calldata_to_MainGUI(booking)
            self.accept()
        except ValueError as e:
            show_error(str(e))
        except Exception as e:
            show_error(f"Terjadi kesalahan: {str(e)}")
