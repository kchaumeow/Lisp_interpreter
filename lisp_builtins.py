from lisp_interpreter import List, Atom, Interpreter


def builtin_define(interpreter: Interpreter, name, value):
    assert isinstance(name, Atom), "WHAT DID YOU WRITE EXACTLY? TRY AGAIN"
    interpreter.env[name.value] = interpreter.execute_ast(value)


def internal_lambda(interpreter: Interpreter, params, expr):
    if isinstance(params, List):
        params = [i.value for i in params.children]
    elif isinstance(params, Atom):
        params = [params.value]

    def func(env, *args):
        env = env.copy()
        env.update(zip(params, args))
        return interpreter.execute_ast(expr, env=env)

    return func


def builtin_if(interpreter: Interpreter, condition_expr, *body):
    condition = interpreter.execute_ast(condition_expr)
    if condition:
        return interpreter.execute_ast(body[0])
    elif len(body) > 1:
        return interpreter.execute_ast(body[1])


def builtin_while(interpreter: Interpreter, condition_expr, body):
    while interpreter.execute_ast(condition_expr):
        interpreter.execute_ast(body)


BUILTIN_ENV = {
    '+': lambda e, a, b: int(a) + int(b),
    '-': lambda e, a, b: int(a) - int(b),
    '*': lambda e, a, b: int(a) * int(b),
    '/': lambda e, a, b: int(a) // int(b),
    '>': lambda e, a, b: int(a) > int(b),
    '<': lambda e, a, b: int(a) < int(b),
    '=': lambda e, a, b: int(a) == int(b),
    '&&': lambda e, a, b: a and b,
    '||': lambda e, a, b: a or b,
    '!': lambda e, a: not a,
    'true': lambda e: True,
    'false': lambda e: False,
    'begin': lambda e, *a: a[-1],
    'print': lambda e, a: print(a),
    'prompt': lambda e: input(),
}

BUILTIN_MACRO = {
    'lambda': internal_lambda,
    'if': builtin_if,
    'while': builtin_while,
    'define': builtin_define
}
