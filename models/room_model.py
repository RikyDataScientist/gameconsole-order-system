from datetime import time

class Room:

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
        self.time_each_rooms = Room.times_available.copy()  # Copy time availability for each rooms.
        self.booked_times = []

    def check_availability(self, selected_time):
        return all(t in self.time_each_rooms for t in selected_time)

    def order(self, selected_time):
        for value in selected_time:
            if value in self.time_each_rooms:
                self.time_each_rooms.remove(value)
                self.booked_times.append(value)

    def get_data(self):
        return {
            "room_id": self.room_id,
            "room_name": self.name_room,
            "status": "available" if len(self.time_each_rooms) > 0 else "unavailable",
            "booked_times": self.booked_times,
        }
