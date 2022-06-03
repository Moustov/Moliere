from canvas.action import Action


class Ability:
    def __init__(self, name: str):
        self.actions = []
        self.name = name

    def enables(self, name: str, action: Action):
        """
        registers some new ability to this actor
        :param name: name of the ability
        :param action: the object associated to the ability
        :return:
        """
        self.actions.append({"name": name, "what": action})
