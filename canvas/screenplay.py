class ScreenPlay:
    """
    """

    def __init__(self, name: str):
        self.name = name

    def is_already_registered(self, name: str, items: [dict]) -> bool:
        """
        Tells if an item name is already in the items list
        :param name:
        :param items: {"name": "XXXX", "what": ScreenPlay}
        :return: True is the name is in items
        """
        for item in items:
            if item["name"] == name:
                return True
        return False

    def ask_questions(self, scenario: dict):
        pass
