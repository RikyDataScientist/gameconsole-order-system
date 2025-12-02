from models.room_model import Room
from utils.json_helpers import load_data, save_data

class RoomManager:
    path = "database/rooms.json"

    def __init__(self, room_id, name_room):
        self.model = Room(room_id, name_room)
        self.data = self.load()
        self.time_in_room = None
        self.booked_times = None

    def load(self):
        data = load_data(RoomManager.path)
        for value in data:
            if self.model.room_id == value["room_id"]:
                self.booked_times = value["booked_times"]
                self.time_in_room = [i for i in self.model.time_each_rooms if i not in self.booked_times]

                self.model.time_each_rooms = self.time_in_room
                self.model.booked_times = self.booked_times

                return value
        return None

    def check_room_general(self):
        return len(self.time_in_room) > 0

    def check_room_by_hour(self, selected_time):
        if not isinstance(selected_time, list):
            selected_time = [selected_time]

        return all(t in self.time_in_room for t in selected_time)

    def order(self, selected_time):
        for value in selected_time:
            if value in self.time_in_room:
                self.booked_times.append(value)
                self.time_in_room.remove(value)

        self.model.time_each_rooms = self.time_in_room
        self.model.booked_times = self.booked_times

        data = load_data(RoomManager.path)
        for a in data:
            if self.model.room_id == a["room_id"]:
                a.update(self.model.get_data(self.time_in_room, self.booked_times))
        save_data(RoomManager.path, data)
