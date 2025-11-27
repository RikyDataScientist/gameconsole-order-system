from datetime import datetime
class Payment:
    sequence = 0

    def __init__(self, booking_id, username, room_id, console, amount, status):
        Payment.sequence += 1
        self.payment_id = str(Payment.sequence)

        self.booking_id = booking_id
        self.username = username
        self.room_id = room_id
        self.console = console
        self.amount = amount
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = status

    def get_dict(self):
        return {
            "payment_id": self.payment_id,
            "booking_id": self.booking_id,
            "username": self.username,
            "room_id": self.room_id,
            "console": self.console,
            "amount": self.amount,
            "time": self.time,
            "status": self.status
        }