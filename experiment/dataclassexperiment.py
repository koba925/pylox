from dataclasses import dataclass, field
from typing import List


@dataclass
class Struct:
    x: str


@dataclass
class Container:
    content: List[Struct] = field(default_factory=list)


@dataclass
class ContainerWrapper:
    container: Container  # `= Container()`をつけるとエラーになる

    def __init__(self) -> None:  # コンストラクタで初期化する
        self.container = Container()

    def append(self, s: Struct) -> None:
        self.container.content.append(s)

    def store_structs(self, s_list: List[Struct]) -> None:
        for s in s_list:
            self.append(s)


struct_list = [Struct("foo")]
ContainerWrapper().store_structs(struct_list)
# recreated instance strangely contains old instance's data.
wrapper = ContainerWrapper()
print(wrapper.container)  # => Container(content=[Struct(x='foo')])
