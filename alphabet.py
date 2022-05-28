from typing import Callable, Iterable


class Alphabet:
    def __init__(
        self,
        index_to_char: Callable[[int], str],
        char_to_index: Callable[[str], int],
        length: int,
    ) -> None:
        self.index_to_char: Callable[[int], str] = index_to_char
        self.char_to_index: Callable[[str], int] = char_to_index
        self.length = length

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, i) -> str:
        return self.index_to_char(i)

    def __iter__(self) -> Iterable[str]:
        for i in range(len(self)):
            yield self[i]

    def index(self, char: str) -> int:
        index = self.char_to_index(char)
        if index >= len(self) or index < 0:
            raise ValueError(f"Character `{char}` is not in the alphabet")
        return index


printable_ascii_letters = Alphabet(lambda x: chr(x + 32), lambda x: ord(x) - 32, 96)

five_letters = Alphabet(lambda x: chr(x + ord("a")), lambda x: ord(x) - ord("a"), 5)

lower_case_ascii_letters = Alphabet(
    lambda x: chr(x + ord("a")), lambda x: ord(x) - ord("a"), 26
)
