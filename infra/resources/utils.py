from re import sub


# example_text
def snake_case(s):
    return "_".join(sub("([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))).split()).lower()


# example-text
def kebab_case(s):
    return "-".join(sub("([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("_", " "))).split()).lower()


# exampleText
def camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


# ExampleText
def pascal_case(s):
    return sub(r"(_|-)+", " ", s).title().replace(" ", "")
