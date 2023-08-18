from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from lox_expr import Expr
from lox_token import Token

R = TypeVar("R")


class StmtVisitor(ABC, Generic[R]):
    @abstractmethod
    def visit_block_stmt(self, stmt: "Block") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_print_stmt(self, stmt: "Print") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_var_stmt(self, stmt: "Var") -> R:
        raise NotImplementedError()


class Stmt:
    @abstractmethod
    def accept(self, visitor: StmtVisitor[R]) -> R:
        raise NotImplementedError()


@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_block_stmt(self)


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_print_stmt(self)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Optional[Expr]

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_var_stmt(self)
