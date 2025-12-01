from datetime import time

class Room:

    times_available = [
        time(9),
        time(10),
        time(11),
        time(12),
        time(13),
        time(14),
        time(15),
        time(16),
        time(17),
    ]

    def __init__(self, room_id, name_room):
        self.room_id = room_id
        self.name_room = name_room
        self.time_each_rooms = Room.times_available.copy()  # Copy time availability for each rooms.
        self.booked_times = []

    def get_data(self, times, booked):
        self.time_each_rooms = times
        self.booked_times = booked
        return {
            "room_id": self.room_id,
            "room_name": self.name_room,
            "status": "available" if len(self.time_each_rooms) > 0 else "unavailable",
            "booked_times": self.booked_times,
        }
