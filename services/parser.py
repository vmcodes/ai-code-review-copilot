import ast

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    functions, classes = [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append((node.name, node.lineno))
        if isinstance(node, ast.ClassDef):
            classes.append((node.name, node.lineno))

    return functions, classes