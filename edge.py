from typing import Iterable


class Pointer:
    def __init__(self, value) -> None:
        self.value = value


class Edge:
    def __init__(
        self,
        string: str,
        end_node,
        global_pointer: Pointer,
        start_index: int,
        end_index: int | None = None,
        is_end: bool = False,
    ) -> None:
        if end_index is None and not is_end:
            raise ValueError(
                "Edges that have an `is_end` value of `False` must have an `end_index`"
            )

        self.string: str = string

        self.end_node = end_node

        self.start_index: int = start_index

        self.is_end: bool = is_end

        self._end_index: int | None = None if is_end else end_index

        self.pointer: Pointer = global_pointer

    @property
    def end_index(self) -> int:
        if self.is_end:
            return self.pointer.value
        else:
            return self._end_index

    @end_index.setter
    def end_index(self, value: int) -> None:
        self._end_index = None if self.is_end else value

    def __len__(self) -> int:
        return self.end_index - self.start_index + 1

    def __getitem__(self, i: int) -> str:
        if i >= len(self):
            raise IndexError("Trying to access character past edge")

        return self.string[self.start_index + i]

    def __iter__(self) -> Iterable[str]:
        for i in range(self.start_index, self.end_index + 1):
            yield self.string[i]


class EdgeFactory:
    def __init__(self, string: str, global_pointer: Pointer) -> None:
        self.string: str = string
        self.global_pointer: Pointer = global_pointer

    def __call__(
        self,
        end_node,
        start_index: int,
        end_index: int | None = None,
        is_end: bool = False,
    ) -> Edge:
        return Edge(
            self.string, end_node, self.global_pointer, start_index, end_index, is_end
        )
