from canvas.action import Action


class Ability:
    def __init__(self):
        self.enables = []

    def add_action(self, name: str, action: Action):
        """
        registers some new ability to this actor
        :param name: name of the ability
        :param action: the object associated to the ability
        :return:
        """
        self.enables.append({"name": name, "what": action})
