from typing import Optional


class Remainder:
    def __init__(self, string: str) -> None:
        self.string: str = string
        self.start_index: int = 0
        self.end_index: int = -1

    def __len__(self) -> int:
        return self.end_index - self.start_index + 1

    @property
    def first_character(self) -> Optional[str]:
        if len(self) == 0:
            return None
        else:
            return self.string[self.start_index]

    def remove_n_from_front(self, n: int) -> None:
        if len(self) < n:
            raise ValueError(
                "Cannot traverse more characters than the amount in the remainder"
            )
        else:
            self.start_index += n

    def add_n_to_back(self, n: int) -> None:
        self.end_index += n

    def shift_n(self, n: int) -> None:
        self.start_index += n
        self.end_index += n
