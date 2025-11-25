from utils.json_helpers import load_data, save_data
from models.user_model import User

class UserController:
    path = 'database/users.json'

    # Username and Password Validation
    @staticmethod
    def validate_username(username):
        if not username:
            raise ValueError('Username tidak boleh kosong')
        if len(username) < 4:
            raise ValueError('Username harus terdiri minimal 4 huruf')

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError('Password minimal terdiri 8 karakter')

    # Method link with Database
    @classmethod
    def load(data):
        return load_data(data.path)

    @classmethod
    def save(data, data_user):
        return save_data(data.path, data_user)

    @classmethod
    def check_username(data, username):  # Check, is username exist in database?
        data_user = data.load()
        return any(u["username"] == username for u in data_user)

    @classmethod
    def search_user(data, username, password=None):  # Check are username(first check) & password exist in database
        data_user = data.load()
        for key in data_user:
            if key['username'] == username:
                if key['password'] == password or password is None:
                    return key
        return None

    # Register or Sign Up Function
    @classmethod
    def register(data, username, password):
        data.validate_username(username)
        data.validate_password(password)

        if data.check_username(username):
            raise ValueError('Username telah digunakan')

        new_data_user = User(username, password)
        all_data = data.load()
        all_data.append(new_data_user.get_data())
        data.save(all_data)

        return 'Registrasi Berhasil'

    # Log in Function
    @classmethod
    def login(data, username, password):
        data.validate_username(username)
        data.validate_password(password)

        data_user = data.search_user(username, password)
        if not data_user:
            raise ValueError('Username atau Password salah')

        return 'Login Berhasil'
