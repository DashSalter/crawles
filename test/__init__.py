import types

def a():
    return 1

def b():
    yield 2

result = b()
if isinstance(result, types.GeneratorType):
    print("result 是生成器对象")
else:
    print("result 不是生成器对象")