from PyQt6.QtWidgets import QApplication, QStackedWidget
from gui.user_log import Login, Register
from controller.user_controller import UserController

if __name__ == "__main__":
    app = QApplication([])

    app.setStyleSheet("""
        QWidget {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI';
        }
""")

    stack = QStackedWidget()
    controller = UserController()

    login = Login(stack, controller)
    signup = Register(stack, controller)

    stack.addWidget(login)
    stack.addWidget(signup)

    stack.setCurrentIndex(0)

    stack.show()
    app.exec()
