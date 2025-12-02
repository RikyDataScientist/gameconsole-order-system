from datetime import datetime
class Payment:
    sequence = 0

    def __init__(self, booking_id, username, room_id, times_book, console, price, status):
        Payment.sequence += 1
        self.payment_id = str(Payment.sequence)

        self.booking_id = booking_id
        self.username = username
        self.room_id = room_id
        self.times_book = times_book
        self.console = console
        self.price = price
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = status

    def get_dict(self):
        return {
            "payment_id": self.payment_id,
            "booking_id": self.booking_id,
            "username": self.username,
            "room_id": self.room_id,
            "time booked": self.times_book,
            "console": self.console,
            "price": self.price,
            "time": self.time,
            "status": self.status
        }
