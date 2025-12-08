from datetime import time

class Room:

    times_available = [time(t) for t in range(8, 18)]

    def __init__(self, room_id, name_room):
        self.room_id = room_id
        self.name_room = name_room
        self.time_each_rooms = Room.times_available.copy()  # Copy time availability for each rooms.
        self.booked_times = []
