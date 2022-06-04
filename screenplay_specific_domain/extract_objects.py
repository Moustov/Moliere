from deepdiff import DeepDiff


def extract_value_between(raw_string, left_delimiter, right_delimiter) -> str:
    """
    return the string between left_delimiter and right_delimiter
    :param raw_string:
    :param left_delimiter:
    :param right_delimiter:
    :return:
    """
    left_right = raw_string.split(left_delimiter)
    value = left_right[1].split(right_delimiter)
    return value[0]


def remove_string_dupes_in_array(an_array: [str]) -> [str]:
    """
    remove dupes in an_array
    :param an_array:
    :return:
    """
    return list(dict.fromkeys(an_array))


def remove_dupes_in_parametrized_array(list_elements: [dict]) -> [dict]:
    elements = []
    for element in list_elements:
        element_found = False
        for element2 in elements:
            diff = DeepDiff(element, element2, ignore_order=True)
            if diff == {}:
                element_found = True
        if not element_found:
            elements.append(element)
    return elements


def remove_dupes_in_elements(list_elements: [dict]) -> [dict]:
    """
    remove dupes in a list_elements [{"item": an item, "screen": the Screen-like name onto which an item can be found}*]
    :param list_elements:
    :return:
    """
    elements = []
    res = []
    for element in list_elements:
        if element["item"] not in elements:
            elements.append(element["item"])
            res.append(element)
    return res


def append_objects(object_name: str, scene1: dict, scene2: dict) -> dict:
    """
    just add the objects from both scene1 and scene2
    :param object_name:
    :param scene1:
    :param scene2:
    :return:
    """
    res_scene = scene1
    if object_name in scene1.keys():
        if object_name in scene2.keys():
            for an_object in scene2[object_name]:
                res_scene[object_name].append(an_object)
    elif object_name in scene2.keys():
        res_scene[object_name] = scene2[object_name]
    else:
        res_scene[object_name] = []
    return res_scene


def merge_simple_object(object_name: str, scene1: dict, scene2: dict) -> dict:
    """
    when a screenplay object has no param (ie this is a simple array of strings), this function can be called to merge
    scenes at the object_name part only
    :param object_name: "actors", "facts", "screens", "abilities"
    :param scene1:
    :param scene2:
    :return:
    """
    res_scene = append_objects(object_name, scene1, scene2)
    res_scene[object_name] = remove_string_dupes_in_array(res_scene[object_name])
    return res_scene


def merge_parametrized_object(object_name: str, scene1: dict, scene2: dict) -> dict:
    """
    when a screenplay object has some param ({"item": "an item", "is": "big"}), this function can be called to merge
    scenes at the object_name part only
    :param object_name: "questions", "elements", "actions"
    :param scene1:
    :param scene2:
    :return:
    """
    res_scene = append_objects(object_name, scene1, scene2)
    res_scene[object_name] = remove_dupes_in_parametrized_array(res_scene[object_name])
    return res_scene


