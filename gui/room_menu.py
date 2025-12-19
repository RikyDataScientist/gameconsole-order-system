from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from datetime import time
from controller.room_controller import RoomManager
from gui.booking import BookingDialog

class RoomGui(QWidget):

    def __init__(self, stack, user):
        super().__init__()
        self.stack = stack
        self.user = user
        self.setFixedSize(650, 430)
        self.setStyleSheet(style())

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        frame = QFrame()
        frame.setObjectName("card")
        main_layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid = QGridLayout(frame)
        self.grid.setContentsMargins(20, 10, 20, 10)
        self.grid.setSpacing(25)

        title = QLabel("Order Room")
        title.setObjectName("title")
        self.grid.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.combo_box = QComboBox()
        self.combo_box.setObjectName("selectbox")

        self.combo_box.addItem("Select Time", None)
        self.combo_box.addItem("All Time", "All")
        for t in range(8, 18):
            self.combo_box.addItem(f"{t}:00", time(t))
        self.grid.addWidget(self.combo_box, 1, 0, 1, 2)
        self.combo_box.setCurrentIndex(self.combo_box.findData("Select Time"))

        self.combo_box.currentIndexChanged.connect(self.update_data)

        self.rooms = [
            RoomManager(1, "Room A"),
            RoomManager(2, "Room B"),
            RoomManager(3, "Room C"),
            RoomManager(4, "Room D")
        ]

        self.button = []
        idx = 0
        for r in range(2, 4):
            for c in range(2):
                btn = QPushButton(self.rooms[idx].model.name_room)
                btn.setFixedSize(150, 90)
                btn.setObjectName("button")
                btn.clicked.connect(lambda checked=False, room=self.rooms[idx]: self.execute(room))
                self.button.append(btn)
                self.grid.addWidget(btn, r, c)
                idx += 1

        cancel_button = QPushButton("Back")
        cancel_button.setFixedSize(100, 35)
        cancel_button.setObjectName("nav_button")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #196c2e;
            }""")
        cancel_button.clicked.connect(self.exit_run)
        self.grid.addWidget(cancel_button, 4, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.update_data()
        self.update_button()

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
                font-size: 16px;
                border-radius: 13px;
                border: 2px solid #58a6ff;
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
                font-size: 16px;
                border: 1px solid #21262d;
                border-radius: 13px;
                }
                """)

    def update_button(self):
        self.combo_box.setCurrentIndex(self.combo_box.findData(None))

    def exit_run(self):
        self.stack.setCurrentIndex(0)
        self.update_data()
        self.update_button()

    def execute(self, which_room):
        selected_time = self.combo_box.currentData()
        room_to_book = BookingDialog(callback=self.stack.parent(), user=self.user, room=which_room, selected_times=selected_time)
        self.update_data()
        self.update_button()
        room_to_book.exec()

def style():
    return """
    #title {
        font-size: 26px;
        font-weight: bold;
        color: #58a6ff;
        background: transparent;
    }

    #selectbox {
        background-color: #0d1117;
        border: 2px solid #30363d;
        padding: 10px;
        border-radius: 10px;
        font-size: 15px;
        color: #c9d1d9;
    }

    #selectbox:hover {
        border: 2px solid #58a6ff;
    }

    #selectbox::drop-down {
        border: none;
        width: 30px;
    }

    #selectbox QAbstractItemView {
        background-color: #161b22;
        color: #c9d1d9;
        selection-background-color: #238636;
        border-radius: 8px;
    }
    """
