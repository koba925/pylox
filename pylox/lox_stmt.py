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
    def visit_function_stmt(self, stmt: "Function") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_if_stmt(self, stmt: "If") -> R:
        raise NotImplementedError

    @abstractmethod
    def visit_print_stmt(self, stmt: "Print") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_return_stmt(self, stmt: "Return") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_var_stmt(self, stmt: "Var") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visit_while_stmt(self, stmt: "While") -> R:
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
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_function_stmt(self)


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_if_stmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_print_stmt(self)


@dataclass
class Return(Stmt):
    keyword: Token
    value: Optional[Expr]

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_return_stmt(self)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Optional[Expr]

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_var_stmt(self)


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_while_stmt(self)
