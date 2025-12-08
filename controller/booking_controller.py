from models.booking import Booking
from utils.json_helpers import load_data, save_data

class BookingController:
    console = {
        "PS5": 15000,
        "PS4": 10000,
        "Xbox Series X": 20000,
        "Nintendo Switch": 18000
    }

    def __init__(self, user, room):
        self.user = user
        self.room = room

    def price(self, console, time_selected):
        price = BookingController.console[console]
        return price * len(time_selected)

    def create_booking(self, console, time_selected):
        if not console:
            raise ValueError("Pilih Jenis Console")
        if not time_selected:
            raise ValueError("Pilih Waktu Bermain")

        path = "database/booking.json"
        data = load_data(path)
        Booking.sequence = len(data)

        time_in_str = [f"{t.hour:02d}:00" for t in time_selected]
        price = self.price(console, time_selected)

        data_booking = Booking(
            username=self.user.username,
            room_id=self.room.model.room_id,
            times=time_in_str,
            console=console,
            price=price
        )

        data.append(data_booking.get_dict())
        save_data(path, data)

        return data_booking
