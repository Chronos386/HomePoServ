class SendPointRoute:
    def __init__(self, x: float, y: float, floor: int, room: str):
        self.x = x
        self.y = y
        self.floor = floor
        self.room = room

    def __dict__(self):
        return {
            'x': self.x,
            'y': self.y,
            'floor': self.floor,
            'room': self.room
        }
