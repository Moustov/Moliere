from screenplay_specific_domain.extract_objects import extract_screenplay_objects, merge_screenplay_objects
from screenplay_specific_domain.skeleton_generator import SkeletonGenerator


class Scene:
    def __init__(self, target_folder: str):
        self.generator = SkeletonGenerator(target_folder)
        self.my_screenplay_objects = {}
        self.my_scenes = []

    def add_moliere_script(self, script_name: str, moliere_script: str, regenerate_project: bool = False):
        """
        adds an acceptance criteria
        :param script_name:
        :param moliere_script: Moliere's BDD - eg.
                GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
                WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                    AND <order> with <999 beers>
                    THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                              THANKS TO <the total amount> FOUND ON <the bill>
        :param regenerate_project: todo propose regenerating/versioning/overlapping
        """
        self.my_scenes.append({"name": script_name, "acceptance criterion": moliere_script})
        new_scene = extract_screenplay_objects(moliere_script)
        self.my_screenplay_objects = merge_screenplay_objects(self.my_screenplay_objects, new_scene)

    def generate_screenplay(self, regenerate_project: bool = False) -> [str]:
        self.generator.generate_skeleton_parts(self.my_screenplay_objects, regenerate_project)
        scenarios = self.generator.generate_questions()


if __name__ == '__main__':
    a_script = """
            GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
    a_scene = Scene()
    a_scene.add_moliere_script("AC #1", a_script)
