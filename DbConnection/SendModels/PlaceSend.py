class PlaceSend:
    def __init__(self, place_id, x, y, is_class, floor, room_name, name, description, photo_name):
        self.id = place_id
        self.x = x
        self.y = y
        self.is_class = is_class
        self.floor = floor
        self.room = room_name
        self.name = name
        self.photo = photo_name
        self.description = description
