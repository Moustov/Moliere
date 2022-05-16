from canvas.ability import Ability


class Actor:
    def __init__(self):
        self.abilities = []

    def add_ability(self, name: str, ability: Ability):
        """
        registers some new ability to this actor
        :param name: name of the ability
        :param ability: the object associated to the ability
        :return:
        """
        self.abilities.append({"name": name, "what": ability})

    def learns(self):
        pass

    def asks(self):
        pass

    def has(self):
        pass

    def performs(self):
        pass