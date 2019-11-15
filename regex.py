from re import sub
from num2words import num2words


def convert(txt):
    return sub(r"(\d+)", lambda x: num2words(int(x.group(0))), txt)
