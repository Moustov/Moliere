# WHAT'S THIS PROJECT ALL ABOUT?
Gherkin extension for [ScreenPlay design pattern](https://ideas.riverglide.com/page-objects-refactored-12ec3541990#.ekkiguobe)(SPDP)
The idea rose from [Micha Kutz' talk on "Writing tests like Shakespeare](https://youtu.be/Ptg5NICosNY?t=5870)

The aim is to extend Gherkin grammar with some extra info to generate class stubs compliant with SPDP
## Gherkin extension
Language definition:
```
GIVEN <Actor> who can <Ability> [and <Ability>]+
WHEN {<Actor> does <Task> {at|with|in} <Parameters>}
                [and <Task> {at|with|in} <Parameters>}]+
THEN <Actor> checks <Question> is <Assertion> THANKS TO <element> FOUND ON <screen>
                [and <Question> is <Assertion> THANKS TO <element> FOUND ON <screen>]+
```
See [tests/test_generate_screenplay.py](https://github.com/Moustov/ScreenPlay_Shakespeare/blob/master/tests/test_generate_screenplay.py)

## Screenplay Overview
```
    @startuml
    ScreenPlay <|-- Actor
    ScreenPlay <|-- Fact
    ScreenPlay <|-- Question
    ScreenPlay <|-- Element
    ScreenPlay <|-- Task
    ScreenPlay <|-- Action
    ScreenPlay <|-- Screen
    Actor "1" o-- "n" Ability : has
    Actor "1" o-- "n" Task : performs
    Actor "1" o-- "n" Question : asks
    Actor "1" o-- "n" Fact : learns/remembers
    Fact "1" o-- "n" Question : enable
    Question "1" o-- "n" Element : about the state of
    Element "1" o-- "n" Screen : on a
    Task "1" o-- "n" Action : made up of
    Ability "1" o-- "n" Action : enables
    Action "1" o-- "n" Element : interacts with
    @enduml
```

Example:\
generated from an SPDP scenario with `extract_questions(scenario)`
```
    an_actor.name = "John"
    element_1.can_be_found_on(page_1)
    element_2.can_be_found_on(page_1)
    element_3.can_be_found_on(page_2)
    element_4.can_be_found_on(page_1)
    element_5.can_be_found_on(page_3)
    action_1.add_interaction(1, element_1)
    action_1.add_interaction(2, element_2)
    action_2.add_interaction(1, element_3)
    action_2.add_interaction(2, element_4)
    a_task.set_sequence([{"task": "sequence #1", 
                        "actions": [{"sequence": 1, "action": action_1}, 
                                    {"sequence": 2, "action": action_2}])
    an_actor.accomplishes(a_task)

    another_actor.name = "a Tester"
    action_3.add_interaction(1, element_4)
    action_4.add_feedback(2, element_5)
    checks_1 = [{"task": "sequence of checks #1", 
                "actions": [{"action": action_3, "sequence": 1},
                            {"check": action_4, "sequence": 2}]
    a_test.set_actions(checks_1)
    feedback = another_actor.accomplishes(checks_1)
    print(feedback)
```    
output:
```
John does the sequence #1
   <action_1.name>\
   and <action_2.name>\
Then a Tester sequence of checks #1
    <action_3.name> 
    and sees 32 EUR on page 5 (element_5)
```
## How to reach the example?
1. ideate SPDP gherkin-like scenarios
2. digest the scenario to generate SPDP classes & tests
3. implement the elements to interact with the screens
4. complete with some logic to implement business process by using elements
5. run the tests


# INSTALLATION
- works python 3.9
- run `pip install -r requirements.txt`
# BUILD

# RUN

# SEE ALSO
- https://github.com/perrygoy/screenpy/blob/trunk/screenpy/actor.py
