from PyQt6.QtWidgets import QApplication, QStackedWidget
from gui.user_log import Login, Register
from controller.user_controller import UserController

app = QApplication([])

stack = QStackedWidget()
controller = UserController()

login = Login(stack, controller)
signup = Register(stack, controller)

stack.addWidget(login)
stack.addWidget(signup)

stack.setCurrentIndex(0)

stack.show()
app.exec()
