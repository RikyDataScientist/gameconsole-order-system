class Booking:
    sequence = 0

    def __init__(self, username, room_id, times, console, price):
        Booking.sequence += 1
        self.booking_id = str(Booking.sequence)

        self.username = username
        self.room_id = room_id
        self.times = times
        self.console = console
        self.price = price
        self.status = "pending"

    def get_dict(self):
        return {
            "booking_id": self.booking_id,
            "username": self.username,
            "room_id": self.room_id,
            "times": self.times,
            "console": self.console,
            "price": self.price,
            "status": self.status
        }
