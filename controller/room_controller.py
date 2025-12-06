from models.room_model import Room
from utils.json_helpers import load_data, save_data

class RoomManager:
    path = "database/rooms.json"

    def __init__(self, room_id, name_room):
        self.model = Room(room_id, name_room)
        self.load()

    def load(self):
        data = load_data(RoomManager.path)
        for value in data:
            if self.model.room_id == value["room_id"]:
                self.model.booked_times = value.get("booked_times", [])
                self.model.time_each_rooms = [i for i in self.model.time_each_rooms if i not in self.model.booked_times]

                return value
        return None

    def check_room_general(self):
        return len(self.model.time_each_rooms) > 0

    def check_room_by_hour(self, selected_time):
        if not isinstance(selected_time, list):
            selected_time = [selected_time]

        return all(t in self.model.time_each_rooms for t in selected_time)

    def order(self, selected_time):
        for value in list(selected_time):
            if value in self.model.time_each_rooms:
                self.model.booked_times.append(value)
                self.model.time_each_rooms.remove(value)

        data = load_data(RoomManager.path)
        for a in data:
            if self.model.room_id == a["room_id"]:
                a.update(self.model.get_data())
        save_data(RoomManager.path, data)
