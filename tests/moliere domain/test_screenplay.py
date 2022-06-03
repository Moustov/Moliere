from unittest import TestCase

from deepdiff import DeepDiff

from canvas.screenplay import ScreenPlay
from moliere_core_domain.scene_setup import Scene
from screenplay_specific_domain.target_languages.python_translator import ClassContentManager, \
    generate_python_file_name, generate_valid_class_name


class TestScreenPlayFiles(TestCase):
    def init_file_based_unit_tests(self, class_to_assess: str) -> dict:
        """

        :param class_to_assess: raw class name from Moliere script line
        :return: {"class_to_assess": class_content, "expected": expected_screenplay_objects}
        """
        folder = "output"
        a_scene = Scene(folder)
        line_1 = """
            GIVEN <Jack Donald> who can <buy some beers>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #1", line_1)
        a_scene.generate_screenplay(regenerate_project=True)
        the_class_name = generate_valid_class_name(class_to_assess)
        a_class = a_scene.generator.screenplay_classes[the_class_name]
        cg = ClassContentManager(folder)
        input_class_path = f"{a_class.target_location}/{generate_python_file_name(a_class.the_class['class_name'])}"
        class_content = cg.set_class_from_file(input_class_path)
        return class_content

    def test_generate_screenplay_objects_actor_file_Jack_Donald_methods(self):
        """"
        we should have exactly 4 methods - no dupes!
        """
        res = self.init_file_based_unit_tests("Jack Donald")
        self.assertTrue(len(res["methods"]) == 4)

    def test_generate_screenplay_objects_actor_file_Jack_Donald(self):
        expected_screenplay_objects = {
            'package': 'output.actors',
            'imports': [],
            'class_name': 'JackDonald',
            'inherits from': ["Actor"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': '        pass'
            }, {
                'name': 'buy_some_beers',
                'parameters': ['self'],
                'return type': 'bool',
                'code': '        print("some code needs to be added in JackDonald.buy_some_beers to interact with the JackDonald is true")\n'
                        '        return False'
            }, {
                'name': 'go_to_the_pub',
                'parameters': ['self'],
                'return type': 'bool',
                'code': '        print("some code needs to be added in JackDonald.go_to_the_pub to interact with the JackDonald is true")\n'
                        '        return False'
            }, {
                'name': 'order',
                'parameters': ['self'],
                'return type': 'bool',
                'code': '        print("some code needs to be added in JackDonald.order to interact with the JackDonald is true")\n'
                        '        return False'
            }
            ],
            'properties': []
        }
        res = self.init_file_based_unit_tests("Jack Donald")
        diff = DeepDiff(res, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_generate_screenplay_objects_actor_file_Jack_Donald_ancestors(self):
        res = self.init_file_based_unit_tests("Jack Donald")
        self.assertTrue("Actor" in res["inherits from"])

    def test_generate_screenplay_objects_ability_file_buy_some_beers(self):
        expected_screenplay_objects = {
            'package': 'output.abilities',
            'imports': [],
            'class_name': 'BuySomeBeers',
            'inherits from': ["Ability"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': '        pass'
            }
            ],
            'properties': []
        }
        res = self.init_file_based_unit_tests("buy some beers")
        diff = DeepDiff(res, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_generate_screenplay_objects_ability_file_buy_some_beers_methods(self):
        res = self.init_file_based_unit_tests("buy some beers")
        self.assertTrue(len(res["methods"]) == 1)

    def test_generate_screenplay_objects_ability_file_buy_some_beers_ancestors(self):
        res = self.init_file_based_unit_tests("buy some beers")
        self.assertTrue("Ability" in res["inherits from"])

    def test_generate_screenplay_objects_action_file_the_sheeps_head_pub(self):
        res = self.init_file_based_unit_tests("The Sheep's Head Pub")
        expected_screenplay_objects = {
            'package': 'output.actions',
            'imports': [],
            'class_name': 'TheSheepsHeadPub',
            'inherits from': ["Action"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': '        pass'
            }
            ],
            'properties': []
        }
        diff = DeepDiff(res, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_generate_screenplay_objects_action_file_the_sheeps_head_pub_method(self):
        res = self.init_file_based_unit_tests("The Sheep's Head Pub")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue(len(res["methods"]) == 1)

    def test_generate_screenplay_objects_action_file_the_sheeps_head_pub_ancestors(self):
        res = self.init_file_based_unit_tests("The Sheep's Head Pub")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue("Action" in res["inherits from"])

    def test_generate_screenplay_objects_screen_file_the_bill(self):
        res = self.init_file_based_unit_tests("the bill")
        expected_screenplay_objects = {
            'package': 'output.screens',
            'imports': ["from output.elements.thetotalamount import TheTotalAmount"],
            'class_name': 'TheBill',
            'inherits from': ["Screen"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': """        a = TheTotalAmount()
        self.add_element(name='TheTotalAmount', element=a)"""
            }
            ],
            'properties': []
        }
        diff = DeepDiff(res, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_generate_screenplay_objects_screen_file_the_bill_method(self):
        res = self.init_file_based_unit_tests("the bill")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue(len(res["methods"]) == 1)

    def test_generate_screenplay_objects_screen_file_the_bill_ancestors(self):
        res = self.init_file_based_unit_tests("the bill")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue("Screen" in res["inherits from"])

    def test_generate_screenplay_objects_element_file_the_total_amount(self):
        res = self.init_file_based_unit_tests("the total amount")
        expected_screenplay_objects = {
            'package': 'output.elements',
            'imports': [],
            'class_name': 'TheTotalAmount',
            'inherits from': ["Element"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': '        pass'
            }
            ],
            'properties': []
        }
        diff = DeepDiff(res, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_generate_screenplay_objects_element_file_the_total_amount_method(self):
        res = self.init_file_based_unit_tests("the total amount")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue(len(res["methods"]) == 1)

    def test_generate_screenplay_objects_element_file_the_total_amount_ancestors(self):
        res = self.init_file_based_unit_tests("the total amount")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue("Element" in res["inherits from"])

    def test_generate_screenplay_objects_task_file_go_to_the_pub(self):
        res = self.init_file_based_unit_tests("???task name???")
        expected_screenplay_objects_action = {
            'package': 'output.tasks',
            'imports': [],
            'class_name': 'JackDonaldGoToThePubTheSheepsHeadPubAndOrder999Beers', # todo name tasks
            'inherits from': ["Task"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': """                an_actor = JackDonal()
        an_element = Element_to_enable_goToThePub()
        a_param = Element_to_reach_TheSheepsHeadPub()
        self.made_up_of(f{"actor": an_actor, "acts on": an_element, "with": a_param})
        an_actor = JackDonal()
        an_element = Element_to_enable_order()
        a_param = Element_to_reach_999Beers()
        self.made_up_of(f{"actor": an_actor, "acts on": an_element, "with": a_param})"""
            }
            ],
            'properties': []
        }
        diff = DeepDiff(res, expected_screenplay_objects_action, ignore_order=True)
        self.assertEqual(diff, {})

        res = self.init_file_based_unit_tests("???question name???")
        expected_screenplay_objects_check = {
            'package': 'output.questions',
            'imports': [],
            'class_name': 'JackDonaldTheTotalAmount999x259EUR', # todo name questions
            'inherits from': ["Question"],
            'lines before fist method': '',
            'methods': [{
                'name': '__init__',
                'parameters': ['self'],
                'return type': '',
                'code': """                an_actor = JackDonal()
        an_element = TheTotalAmount()
        a_param = Is999_259EUR()
        self.made_up_of(f{"actor": an_actor, "acts on": an_element, "with": a_param})"""
            }
            ],
            'properties': []
        }
        diff = DeepDiff(res, expected_screenplay_objects_check, ignore_order=True)
        self.assertEqual(diff, {})

    def test_generate_screenplay_objects_task_file_go_to_the_pub_method(self):
        res = self.init_file_based_unit_tests("go to the pub")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue(len(res["methods"]) == 1)

    def test_generate_screenplay_objects_task_file_go_to_the_pub_ancestors(self):
        res = self.init_file_based_unit_tests("go to the pub")
        # we should have exactly 1 methods - no dupes!
        self.assertTrue("Task" in res["inherits from"])


class TestScreenPlay(TestCase):
    def test_add_moliere_script_more_actions(self):
        a_scene = Scene("output")
        line_1 = """
            GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #1", line_1)
        line_2 = """
            GIVEN <Jack Donald> who can <play music>
            WHEN <Jack Donald> does <play music> at <The Sheep's Head Pub>
                THEN <Jack Donald> checks <the gig reward> is <500 EUR>
                          THANKS TO <earned money> FOUND ON <the table>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #2", line_2)
        expected_screenplay_objects = {
            "actors": ["Jack Donald"],
            "facts": [],
            "tasks": ["go to the pub", "order", "play music"],
            "questions": [{"check": "the total amount", "is": "999 × 2.59 EUR"},
                          {"check": "the gig reward", "is": "500 EUR"}],
            "elements": [{"item": "element_to_reach_The Sheep's Head Pub", "screen": None},
                         {"item": "element_to_enable_browse the web", "screen": None},
                         {"item": "element_to_enable_call HTTP APIs", "screen": None},
                         {"item": "element_to_enable_go to the pub", "screen": None},
                         {"item": "element_to_enable_order", "screen": None},
                         {"item": "element_to_reach_999 beers", "screen": None},
                         {"item": "element_to_enable_play music", "screen": None},
                         {"item": "the total amount", "screen": "the bill"},
                         {"item": "earned money", "screen": "the table"}
                         ],
            "screens": ["the bill", "the table"],
            "abilities": ["browse the web", "call HTTP APIs", "go to the pub", "order", "play music"],
            "actions": [
                {"do": "go to the pub", "direct object": "The Sheep's Head Pub"},
                {"do": "play music", "direct object": "The Sheep's Head Pub"},
                {"do": "order", "direct object": "999 beers"}
            ]
        }
        diff = DeepDiff(a_scene.my_screenplay_objects, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_add_moliere_script_more_actors(self):
        a_scene = Scene("output")
        line_1 = """
            GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #1", line_1)
        line_2 = """
            GIVEN <Bill Evans> who can <play music>
            WHEN <Bill Evans> does <play music> at <The Sheep's Head Pub>
                THEN <Bill Evans> checks <the gig reward> is <5000 EUR>
                          THANKS TO <earned money> FOUND ON <the table>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #2", line_2)
        expected_screenplay_objects = {
            "actors": ["Jack Donald", "Bill Evans"],
            "facts": [],
            "tasks": ["go to the pub", "order", "play music"],
            "questions": [{"check": "the total amount", "is": "999 × 2.59 EUR"},
                          {"check": "the gig reward", "is": "5000 EUR"}],
            "elements": [{"item": "element_to_reach_The Sheep's Head Pub", "screen": None},
                         {"item": "element_to_enable_browse the web", "screen": None},
                         {"item": "element_to_enable_call HTTP APIs", "screen": None},
                         {"item": "element_to_enable_go to the pub", "screen": None},
                         {"item": "element_to_enable_order", "screen": None},
                         {"item": "element_to_reach_999 beers", "screen": None},
                         {"item": "element_to_enable_play music", "screen": None},
                         {"item": "the total amount", "screen": "the bill"},
                         {"item": "earned money", "screen": "the table"}
                         ],
            "screens": ["the bill", "the table"],
            "abilities": ["browse the web", "call HTTP APIs", "go to the pub", "order", "play music"],
            "actions": [
                {"do": "go to the pub", "direct object": "The Sheep's Head Pub"},
                {"do": "play music", "direct object": "The Sheep's Head Pub"},
                {"do": "order", "direct object": "999 beers"}
            ]
        }
        diff = DeepDiff(a_scene.my_screenplay_objects, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})

    def test_play_test_script(self):
        test_script = """        Act 1 - scene 1 - "John" does "sequence #1"
            # SCENE SETUP
                an_actor.name = "John"
                element_1.can_be_found_on(page_1)
                element_2.can_be_found_on(page_1)
                element_3.can_be_found_on(page_2)
                element_4.can_be_found_on(page_1)
                element_5.can_be_found_on(the_mailbox)
                action_1.add_interaction(element_1)
                action_2.add_interaction(element_3)
                a_task.set_sequence([{"task": "sequence #1", 
                                    "actions": [{"sequence": 1, "action": action_1, "param": 123}, 
                                                {"sequence": 2, "action": action_2, "param": click}])
            # SCENE PLAY
                an_actor.accomplishes(a_task)

        Act 1 - scene 1 - "a Tester" does "sequence #1"
            # SCENE SETUP
                another_actor.name = "a Tester"
                action_3.add_interaction(element_4)
                action_4.add_feedback(element_5)
                checks_1 = [{"task": "sequence of checks #1", 
                            "actions": [{"action": action_3, "sequence": 1, "param": 456},
                                        {"check": action_4, "sequence": 2}]
            # SCENE PLAY
                a_test.set_actions(checks_1)
                feedback = another_actor.accomplishes(checks_1)
                print(feedback)
"""
        expected_output = """John does the sequence #1
    -> <action_1.name> with 123 on element_1 in page 1
    -> and <action_2.name> with a click on element_3 in page 2
Then a Tester does the sequence of checks #2
    -> <action_3.name> with 456
    <- and sees 32 EUR from element_5 in the_mailbox"""
        my_comedy = ScreenPlay("Much ado about nothing")
        output = my_comedy.play_test_script("act 1", test_script)
        print(output)
        self.assertEqual(output, expected_output)

