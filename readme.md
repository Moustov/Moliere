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
# INSTALLATION
- works python 3.9
- run `pip install -r requirements.txt`
# BUILD

# RUN
