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
