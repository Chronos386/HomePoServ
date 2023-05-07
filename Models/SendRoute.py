from Models.SendPointRoute import SendPointRoute


class SendRoute:
    def __init__(self, distance: float, route: list[SendPointRoute]):
        self.distance: float = distance
        self.route: list[SendPointRoute] = route
