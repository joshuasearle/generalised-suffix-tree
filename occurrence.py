from dataclasses import dataclass


@dataclass
class Occurrence:
    text_index: int
    suffix_start_index: int
