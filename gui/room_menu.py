from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from datetime import time
from controller.room_controller import RoomManager

class RoomGui(QWidget):

    def __init__(self, user, stack):
        super().__init__()
        self.user = user
        self.stack = stack
        self.setFixedSize(650, 430)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(18)
        self.setLayout(main_layout)

        title = QLabel("Order Room")
        title.setObjectName("title")
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Time Select
        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(200)
        self.combo_box.setObjectName("box")

        self.combo_box.addItem("Select Time", None)
        self.combo_box.addItem("All Time", "All")
        for t in range(9, 18):
            self.combo_box.addItem(f"{t}:00", time(t))

        self.combo_box.currentIndexChanged.connect(self.update_data)
        main_layout.addWidget(self.combo_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # Tombol Room
        self.card = QGridLayout()
        self.card.setSpacing(15)
        self.card.setObjectName("card")
        main_layout.addLayout(self.card)
        main_layout.addStretch()

        self.rooms = [
            RoomManager(1, "Room A"),
            RoomManager(2, "Room B"),
            RoomManager(3, "Room C"),
            RoomManager(4, "Room D")
        ]

        self.button = []
        idx = 0
        for r in range(2):
            for c in range(2):
                btn = QPushButton(self.rooms[idx].model.name_room)
                btn.setFixedSize(150, 90)
                btn.setObjectName("button")
                # btn.clicked.connect()
                self.button.append(btn)
                self.card.addWidget(btn, r, c)
                idx += 1

        self.update_data()

    def update_data(self):
        selected_time = self.combo_box.currentData()

        for button, room in zip(self.button, self.rooms):
            if selected_time is None:
                is_available = room.check_room_general()
            elif selected_time == "All":
                is_available = room.check_room_general()
            else:
                is_available = room.check_room_by_hour(selected_time)

            if is_available:
                button.setEnabled(True)
                button.setStyleSheet("""
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
                """)
            else:
                button.setEnabled(False)
                button.setStyleSheet("""
            #button {
                background-color: #30363d;
                color: #8b949e;
                border: 1px solid #21262d;
                border-radius: 13px;
                }
                """)
