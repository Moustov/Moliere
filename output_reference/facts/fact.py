from output_reference.questions.question import Question
from output_reference.screenplay import ScreenPlay


class Fact (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        pass

    def enable(self, a_question: Question):
        pass
