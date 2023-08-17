from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from lox_token import Token

R = TypeVar("R")


class ExprVisitor(ABC, Generic[R]):
    @abstractmethod
    def visit_assign_expr(self, expr: "Assign") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_binary_expr(self, expr: "Binary") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_grouping_expr(self, expr: "Grouping") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_literal_expr(self, expr: "Literal") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_unary_expr(self, expr: "Unary") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_variable_expr(self, expr: "Variable") -> R:
        raise NotImplementedError()


class Expr:
    @abstractmethod
    def accept(self, visitor: ExprVisitor[R]) -> R:
        raise NotImplementedError()


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_assign_expr(self)


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_unary_expr(self)


@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_variable_expr(self)
