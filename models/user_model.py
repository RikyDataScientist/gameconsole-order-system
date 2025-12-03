from datetime import datetime

class User:
    sequence = 0

    def __init__(self, username, password):
        self.username = username
        self.password = password

        User.sequence += 1
        today = datetime.now().strftime('%Y%m%d')
        self.user_id = f"{today}{User.sequence:03d}"

    # To get instance property in dictionary form
    def get_data(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(data["username"], data["password"])
        obj.user_id = data["user_id"]
        return obj