import unicodedata


def translate_to_python_names(a_name) -> str:
    """
    translates a string into something compatible with python
    see https://stackoverflow.com/questions/2365411/convert-unicode-to-ascii-without-errors-in-python
    todo: use phonetic eg. if japanese "あ" could be translated to "a"
    (see eg https://programminghistorian.org/en/lessons/transliterating)
    :param a_name:
    :return:
    """
    return unicodedata.normalize('NFKD', a_name).encode('ascii', 'ignore').decode()


def generate_valid_class_name(class_name: str) -> str:
    """Turns a class name into PEP8 standard (ie. with CamelCase)
    :param class_name: a class name
    """
    class_name = translate_to_python_names(class_name)
    words = class_name.split(" ")
    res = ""
    for word in words:
        word = word.replace("'", "")
        if word[0].isdigit():
            res += "Some" + word
        else:
            res += word[0].upper() + word[1:]
    return res


def generate_valid_method_name(method_name: str) -> str:
    """
    Turns a method_name name into PEP8 standard (ie. with '_')
    :param method_name:
    :return:
    """
    method_name = translate_to_python_names(method_name)
    res = ""
    for c in method_name:
        if ord('0') <= ord(c) <= ord('9') \
                or ord('a') <= ord(c) <= ord('z') \
                or ord('A') <= ord(c) <= ord('Z'):
            res += c
        elif ord(c) == ord("*") or ord(c) == ord("×"):
            res += "x"
        else:
            res += "_"
    return res


def generate_constructor(properties: [dict]) -> str:
    """
    :param properties:
    :return:
    """
    parameters = ""
    initialize_code = ""
    for a_property in properties:
        if "default value" in a_property.keys() and a_property["default value"] is not None:
            parameters += f", {a_property['name']}=\"{a_property['default value']}\""
        else:
            parameters += ", " + a_property["name"]
        initialize_code += f"\n    self.{a_property['name']} = {a_property['name']}"
    code = f"def __init__(self{parameters}):{initialize_code}\n"
    return code


def serialize_class_definition(json_class: dict):
    class_file_path : json_class["package"]
    with open(class_file_path, "w") as class_file:
        ancestors_string = ""
        if len(json_class["inherits from"]) > 0:
            ancestors_string = "(" + ", ".join(json_class["inherits from"]) + ")"
        class_file.write(f"class {json_class['class_name']} {ancestors_string}:")
        init_method = generate_constructor(json_class["properties"])
        class_file.write(init_method)
