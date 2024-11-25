import re
 
MODULES = {
    "mod1": 'print("first module loaded");',
    "mod2": 'print("second module loaded");'
}

IMPORT_PATTERN = r"\$add\b\s+\b(?P<moduleName>\w+)\b"


# test = "jlsfjlsa sfjlsl; &adjjf &add start &add     end"

# for match in re.finditer(IMPORT_PATTERN, test):
#     print(match.group("moduleName"))

def replace_module(match):
    module_name = match.group("moduleName")
    if module_name in MODULES:
        return MODULES[module_name]
    else:
        raise KeyError(f"The {module_name} module doesn't exist.")

def preprocess(code):
    pure_HLL = re.sub(IMPORT_PATTERN, replace_module, code)

    return pure_HLL 