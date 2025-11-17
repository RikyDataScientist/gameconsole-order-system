from datetime import time


class Room:
    console_charge = {"PS5": 13000, "PS4": 10000, "PS3": 8000, "PS2": 3000}

    times_available = [
        time(8),
        time(9),
        time(10),
        time(11),
        time(14),
        time(15),
        time(16),
        time(17),
    ]

    def __init__(self, room_id, name_room):
        self.room_id = room_id
        self.name_room = name_room
        self.time_each_rooms = (
            Room.times_available.copy()
        )  # Copy time availability for each rooms.
        self.booked_times = []

    def check_availability(self, selected_time):
        return selected_time in self.time_each_rooms

    def order(self, selected_time):
        booked = []
        for value in selected_time:
            if value in self.time_each_rooms:
                self.time_each_rooms.remove(value)
                self.booked_times.append(value)
                booked.append(value)

        return {
            "room_id": self.room_id,
            "room_name": self.name_room,
            "status": "available" if len(self.time_each_rooms) > 0 else "unavailable",
            "booked_times": booked,
        }

    def price(self, console, selected_time):
        console = str(console).upper()
        if console not in Room.console_charge:
            raise ValueError("Jenis console tidak tersedia")

        price_per_hour = Room.console_charge[console]
        total_pay = price_per_hour * len(selected_time)
        return total_pay
