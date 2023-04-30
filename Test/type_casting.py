import ast

_k = ["name", "value", "inline"]
x = "['안녕하세요', '반갑습니다', False]"

n = ast.literal_eval(x)
print(type(n[2]))
