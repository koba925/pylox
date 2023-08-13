from dataclasses import dataclass

from functools import singledispatch

@dataclass
class Expr:
    pass

@dataclass
class NumberLiteral(Expr):
    value: int

@dataclass
class UnaryMinus(Expr):
    right: Expr

@dataclass
class NotImplementedExpr(Expr):
    pass

@singledispatch
def interpret(expr: Expr) -> int:
    raise NotImplementedError(f"Cannot interpret {expr}")

@interpret.register
def _(expr: NumberLiteral) -> int:
    return expr.value

@interpret.register
def _(expr: UnaryMinus) -> int:
    return -1 * interpret(expr.right)

print(interpret(UnaryMinus(UnaryMinus(UnaryMinus(NumberLiteral(3))))))
print(interpret(NotImplementedExpr()))
