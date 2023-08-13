from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from lox_expr import Expr

R = TypeVar("R")


class StmtVisitor(ABC, Generic[R]):
    @abstractmethod
    def visitExpressionStmt(self, stmt: "Expression") -> R:
        raise NotImplementedError()

    @abstractmethod
    def visitPrintStmt(self, stmt: "Print") -> R:
        raise NotImplementedError()


class Stmt:
    @abstractmethod
    def accept(self, visitor: StmtVisitor[R]) -> R:
        raise NotImplementedError()


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visitExpressionStmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visitPrintStmt(self)
