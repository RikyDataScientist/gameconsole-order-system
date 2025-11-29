from PyQt6.QtWidgets import QApplication, QStackedWidget
from gui.user_log import Login, Register
from controller.user_controller import UserController

if __name__ == "__main__":
    app = QApplication([])

    stack = QStackedWidget()
    controller = UserController()

    login = Login(stack, controller)
    signup = Register(stack, controller)

    stack.addWidget(login)
    stack.addWidget(signup)

    stack.setCurrentIndex(0)

    stack.show()
    frame = stack.frameGeometry()
    center = stack.screen().availableGeometry().center()
    frame.moveCenter(center)
    stack.move(frame.topLeft())

    app.exec()
