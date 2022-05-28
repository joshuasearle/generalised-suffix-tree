from random import choices, randint
from string import ascii_lowercase
from generalised_suffix_tree import GeneralisedSuffixTree
from alphabet import printable_ascii_letters

i = 0

while True:
    t = GeneralisedSuffixTree(printable_ascii_letters)
    print(i)

    char_set = ascii_lowercase[: randint(3, 26)]

    for _ in range(300):
        # Make gst with 500 stings of random length from random char set
        a = choices(char_set, k=randint(10, 300))
        a.append("$")
        t.add_string("".join(a))

    for _ in range(100):
        pat = "".join(choices(char_set, k=randint(5, 9)))
        for occ in t.substring_occurrences(pat):
            print(occ)

    i += 1
