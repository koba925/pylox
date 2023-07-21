from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any

from lox_token import Token

R = TypeVar("R")

class Visitor(ABC, Generic[R]):
    @abstractmethod
    def visitBinaryExpr(self, expr: "Binary") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visitGroupingExpr(self, expr: "Grouping") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visitLiteralExpr(self, expr: "Literal") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visitUnaryExpr(self, expr: "Unary") -> R:
        raise NotImplementedError()

class Expr:
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R:
        raise NotImplementedError()


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "Visitor[R]") -> R:
        return visitor.visitBinaryExpr(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visitGroupingExpr(self)

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: "Visitor[R]") -> R:
        return visitor.visitLiteralExpr(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: "Visitor[R]") -> R:
        return visitor.visitUnaryExpr(self)
