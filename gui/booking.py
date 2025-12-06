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
    def __init__(self, user, room, selected_times):
        super().__init__()
        self.selected_times = selected_times
        self.book = BookingController(user=user, room=room)  # Sesuaikan dengan user dan room yang sebenarnya
        self.setWindowTitle("Sistem Booking Console")

        # ======================================================
        # ➜ PERBESAR UKURAN QDIALOG
        # ======================================================
        self.resize(650, 430)

        # ======================================================
        # ➜ SETTING FONT BESAR UNTUK SEMUA ELEMEN
        # ======================================================
        font_besar = QFont("Arial", 14)
        self.setFont(font_besar)

        layout = QVBoxLayout()
        layout.setSpacing(20)     # Jarak antar elemen lebih lega
        layout.setContentsMargins(40, 40, 40, 40)

        # Judul Form
        title_label = QLabel("Booking {self.book.room.room_name}")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # -----------------------------
        # PILIH WAKTU
        # -----------------------------
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
                self.btn.setFixedSize(100, 40)
                self.buttons.append(self.btn)
                h1.addWidget(self.btn, row, col)
        layout.addWidget(frame)

        # -----------------------------
        # PILIH CONSOLE
        # -----------------------------
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Pilih Console:"))

        self.combo_console = QComboBox()
        self.combo_console.setObjectName("box")
        self.combo_console.addItems(["PS5", "PS4", "Xbox Series X", "Nintendo Switch"])
        self.combo_console.setMinimumWidth(300)
        h2.addWidget(self.combo_console)
        layout.addLayout(h2)

        # -----------------------------
        # Harga Total
        # -----------------------------
        h3 = QVBoxLayout()
        self.price_label = QLabel("Harga Total: Rp0")
        h3.addWidget(self.price_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(h3)

        # -----------------------------
        # TOMBOL SIMPAN
        # -----------------------------
        self.btn_simpan = QPushButton("Simpan Booking")
        self.btn_simpan.setMinimumHeight(50)
        self.btn_simpan.setStyleSheet("font-size: 18px;")
        self.btn_simpan.clicked.connect(self.simpan_booking)
        layout.addWidget(self.btn_simpan)

        self.setLayout(layout)
        self.update_buttons()
        self.combo_console.currentIndexChanged.connect(self.update)
        self.findChildren(QPushButton, "button")[0].clicked.connect(self.update)

    # ======================================================
    # Update Tombol Berdasarkan Waktu yang room sudah dipesan
    # ======================================================
    def update_buttons(self):
        if self.selected_times is None or self.selected_times == "All":
            return

        for btn in self.buttons:
            hour = int(btn.text().split(":")[0])
            if hour in self.selected_times:
                btn.setchecked(True)
                break

    # ======================================================
    # Update Harga Total Saat Pilihan Berubah
    # ======================================================
    def update(self):
        selected_console = self.combo_console.currentText()
        selected_button = self.findChildren(QPushButton, "button")
        selected_times = [time(int(btn.text().split(":")[0])).hour for btn in selected_button if btn.isChecked()]

        if not selected_times:
            self.price_label.setText("Harga Total: Rp0")
            return

        total_price = self.book.price(selected_console, selected_times)
        self.price_label.setText(f"Harga Total: Rp{total_price}")

    # ======================================================
    # Tombol Simpan Booking
    # ======================================================
    def simpan_booking(self):
        selected_console = self.combo_console.currentText()
        selected_button = self.findChildren(QPushButton, "button")
        selected_times = [time(int(btn.text().split(":")[0])).hour for btn in selected_button if btn.isChecked()]

        if not selected_times:
            show_error("Silakan pilih minimal satu waktu booking.")
            return

        try:
            booking = self.book.create_booking(selected_console, selected_times)
            self.book.room.order(selected_times)
            show_info(f"Booking berhasil!\nID Booking: {booking.booking_id}\nTotal Harga: Rp{booking.price}")
        except ValueError as e:
            show_error(str(e))
