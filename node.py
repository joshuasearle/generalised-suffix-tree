from occurrence import Occurrence
from edge import Edge
from alphabet import Alphabet


class Node:
    def __init__(
        self,
        alphabet: Alphabet,
        is_root: bool = False,
        is_leaf: bool = False,
    ) -> None:
        self.is_root: bool = is_root
        self.is_leaf: bool = is_leaf

        self.alphabet: Alphabet = alphabet
        self.edges: list[Edge | None] = [None for _ in alphabet]
        self.suffix_link: Node | None = None

        self.suffix_occurrences: list[Occurrence] = []

    def add_suffix(self, text_index: int, suffix_start_index: int):
        self.suffix_occurrences.append(Occurrence(text_index, suffix_start_index))

    def __getitem__(self, character: str) -> Edge | None:
        return self.edges[self.alphabet.index(character)]

    def __setitem__(self, character: str, edge: Edge) -> None:
        self.edges[self.alphabet.index(character)] = edge

    def __contains__(self, character: str) -> bool:
        return self.edges[self.alphabet.index(character)] is not None

    def __iter__(self):
        for edge in self.edges:
            if edge is not None:
                yield edge


class NodeFactory:
    def __init__(self, alphabet: Alphabet) -> None:
        self.alphabet: Alphabet = alphabet

    def __call__(
        self,
        is_root: bool = False,
        is_leaf: bool = False,
    ):
        return Node(self.alphabet, is_root, is_leaf)
