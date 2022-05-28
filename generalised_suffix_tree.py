from typing import Generator
from occurrence import Occurrence
from alphabet import Alphabet, printable_ascii_letters
from node import NodeFactory, Node
from edge import EdgeFactory, Pointer, Edge
from remainder import Remainder


class GeneralisedSuffixTree:
    def __init__(self, alphabet: Alphabet) -> None:
        self.alphabet: Alphabet = alphabet
        self.strings: list[str] = []

        self.phase: int = 0
        self.j: int = 0
        self.last_j: int = -1

        # self.global_pointer = Pointer(0)

        self.node_factory = NodeFactory(alphabet)
        # self.edge_factory = EdgeFactory(strings[0], alphabet)

        self.root = self.node_factory(is_root=True)
        self.root.suffix_link = self.root

        self.active_node: Node = self.root
        # self.remainder = Remainder(strings[0])

        self.pending: Node | None = None

        # Used for signalling main loop rule 3 was found
        self.stop_extensions: bool = False

        self.text_index = -1

    def add_string(self, string):
        self.text_index += 1
        self.strings.append(string)

        # Create a new pointer for each string added
        self.global_pointer = Pointer(0)

        self.edge_factory = EdgeFactory(string, self.global_pointer)
        self.remainder = Remainder(string)

        self.last_j = -1
        self.active_node = self.root
        self.pending = None

        for self.phase in range(len(string)):

            # Implicitly extend all leaf edges (rule 1 extensions)
            self.global_pointer.value = self.phase

            # Reset flag at phase start
            self.stop_extensions = False

            for self.j in range(self.last_j + 1, self.phase + 1):

                if self.stop_extensions:
                    break

                self.update_active_data()
                self.make_extension()

    def update_active_data(self) -> None:
        while self.active_data_update_required():
            n = len(self.active_edge)
            self.active_node = self.active_edge.end_node
            self.remainder.remove_n_from_front(n)

    def active_data_update_required(self) -> bool:
        if len(self.remainder) == 0:
            return False
        else:
            return len(self.active_edge) <= len(self.remainder)

    def make_extension(self) -> None:

        end_of_string = self.next_character == "$"

        if len(self.remainder) == 0:
            if self.next_character in self.active_node:
                if end_of_string:
                    # If end of string, don't rule 3 and instead add an occurrence
                    self.handle_add_suffix_to_leaf()
                else:
                    self.handle_rule3()
            else:
                self.handle_rule2a()
        else:
            if self.next_character == self.existing_character:
                if end_of_string:
                    # If end of string, don't rule 3 and instead add an occurrence
                    self.handle_add_suffix_to_edge_end()
                else:
                    self.handle_rule3()
            else:
                self.handle_rule2b()

    def handle_rule2a(self) -> None:
        leaf = self.node_factory(is_leaf=True)
        leaf.add_suffix(text_index=self.text_index, suffix_start_index=self.j)

        edge = self.edge_factory(end_node=leaf, start_index=self.phase, is_end=True)

        self.active_node[self.next_character] = edge

        self.last_j = self.j

        self.resolve_suffix_link_for_existing_node()
        self.traverse_suffix_link()

    def handle_rule2b(self) -> None:
        leaf = self.node_factory(is_leaf=True)
        leaf.add_suffix(text_index=self.text_index, suffix_start_index=self.j)

        new_edge = self.edge_factory(end_node=leaf, start_index=self.phase, is_end=True)

        split_edge_end_start_index = self.active_edge.start_index + len(self.remainder)
        split_edge_end = self.edge_factory(
            end_node=self.active_edge.end_node,
            start_index=split_edge_end_start_index,
            end_index=self.active_edge.end_index,
            is_end=self.active_edge.is_end,
        )

        split_edge_end.pointer = self.active_edge.pointer
        split_edge_end.string = self.active_edge.string

        internal_node = Node(self.alphabet)
        internal_node[self.existing_character] = split_edge_end
        internal_node[self.next_character] = new_edge

        self.active_edge.end_node = internal_node
        self.active_edge.is_end = False
        self.active_edge.end_index = split_edge_end_start_index - 1

        self.last_j = self.j

        self.resolve_suffix_link_for_new_node(internal_node)
        self.pending = internal_node
        self.traverse_suffix_link()

    def handle_rule3(self) -> None:
        self.stop_extensions = True

        self.remainder.add_n_to_back(1)

        self.resolve_suffix_link_for_existing_node()

    def handle_add_suffix_to_leaf(self):
        end_edge = self.active_node[self.next_character]
        leaf: Node = end_edge.end_node
        leaf.add_suffix(text_index=self.text_index, suffix_start_index=self.j)

        self.resolve_suffix_link_for_existing_node()
        self.traverse_suffix_link()

    def handle_add_suffix_to_edge_end(self):
        leaf = self.active_edge.end_node
        leaf.add_suffix(text_index=self.text_index, suffix_start_index=self.j)

        self.resolve_suffix_link_for_existing_node()
        self.traverse_suffix_link()

    def resolve_suffix_link_for_existing_node(self) -> None:
        if self.pending is None:
            return

        self.pending.suffix_link = self.active_node
        self.pending = None

    def resolve_suffix_link_for_new_node(self, internal_node: Node) -> None:
        if self.pending is None:
            return

        self.pending.suffix_link = internal_node
        self.pending = None

    def traverse_suffix_link(self) -> None:
        if self.active_node.is_root and len(self.remainder) != 0:
            self.remainder.remove_n_from_front(1)
        elif self.active_node.is_root:
            self.remainder.shift_n(1)

        self.active_node = self.active_node.suffix_link

    @property
    def next_character(self) -> str:
        """
        The character we are adding in the current phase
        """
        return self.strings[self.text_index][self.phase]

    @property
    def existing_character(self) -> str | None:
        """
        When remainder is not empty,
        the existing character is the character in the location
        we are trying to add the `next_character`.
        If the `next_character` mismatches the `existing_character`,
        a rule 2b extension is needed.
        If the length of the remainder exceeds the length of the active edge,
        we also return `None` to avoid an index error.
        """
        active_edge = self.active_edge

        if active_edge is None:
            return None
        elif len(self.remainder) > len(self.active_edge):
            return None
        else:
            return self.active_edge[len(self.remainder)]

    @property
    def active_edge(self) -> Edge | None:
        """
        When remainder is not empty,
        the active edge is the edge we are looking at.
        """
        if len(self.remainder) == 0:
            return None
        return self.active_node[self.remainder.first_character]

    def substring_occurrences(self, pat: str) -> Generator[Occurrence, None, None]:
        if len(pat) == 0:
            return

        i = 0
        current_node = self.root
        current_edge = self.root[pat[i]]

        while not current_node.is_leaf and current_edge is not None:

            if i + len(current_edge) > len(pat):
                break

            for j, character in enumerate(current_edge):
                if pat[i + j] != character:
                    return

            i += len(current_edge)
            current_node = current_edge.end_node
            current_edge = None if i == len(pat) else current_node[pat[i]]

        # Reached a leaf or an internal node the doesn't contain the next character
        # This means the substring is not in the suffix tree
        if i != len(pat) and current_edge is None:
            return

        # This means the rest of the pattern could lie within the current edge
        # We need to check if the rest of the pattern matches
        if i != len(pat) and current_edge is not None:
            for j in range(i, len(pat)):
                if pat[j] != current_edge[j - i]:
                    return

            # Need to traverse to node at the end
            current_node = current_edge.end_node

        # This means the tested substring ends with `$`,
        # or the tested suffix only has one occurrence with the suffix tree
        # We need to `yield` the suffix, but then we can immediately end
        if current_node.is_leaf:
            for occurrence in current_node.suffix_occurrences:
                yield occurrence
            return

        # We are at an internal node or on an edge
        # We need to DFS to find all leaf nodes from this node

        stack: list[Node] = []

        # Keep going until we both have no nodes remaining,
        # and the current node is a leaf node
        while not current_node.is_leaf or len(stack) != 0:
            for edge in current_node:
                stack.append(edge.end_node)

            current_node = stack.pop()

            if current_node.is_leaf:
                for occurrence in current_node.suffix_occurrences:
                    yield occurrence


def main():
    t = GeneralisedSuffixTree(printable_ascii_letters)

    t.add_string("shineonyoucrazydiamond$")
    t.add_string("lucyintheskywithdiamonds$")


if __name__ == "__main__":
    main()
