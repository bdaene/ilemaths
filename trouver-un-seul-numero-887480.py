# See https://www.ilemaths.net/sujet-trouver-un-seul-numero-887480.html
from itertools import combinations, permutations
from random import choice, shuffle
from string import ascii_letters
from typing import Protocol, Optional, Iterator

"""
Cards have a face value and a back value. There is 't' cards.
The goal of the player is to find the back value of at least one card. The goal of the engine is to prevent it.
At each turn the player choose 'p' cards and the engine gives the back value of one of them.

For a given p, there is limit g(p) such that for all t >= g(p) the player can win no matter what the engine does.
For example g(2) = 4.

For example, for p = 2 and t = 3, the engine can propose:
ab -> 0     
ac -> 1
bc -> 2

But for p = 2 and t = 4, the engine has no solution:
ab -> 0
ac -> 1 (if 0 then a = 0)
ad -> 2 (0 => a = 0, 1 => a = 1)
bc -> 3 (0 => b = 0, 1 => c = 1, 2 impossible because in ad)
bd -> ? (0 => b = 0, 1 impossible, 2 => d = 2, 3 => b = 3)
cd -> ? (0 impossible, 1 => c = 1, 2 => d = 2, 3 => c = 3)


If the engine is able to generate two permutations with no value aligned such that there is always at least one common 
value for each combination of card then it can answer this common value and there is no way to differentiate between
the permutation. The engine wins.

One can show that those permutations are valid and are the longest possible for a given p:
abcdefghi...
012345678...
120453786...  

If t is not a multiple of 3, we can use pairs instead of triplets like this:
abcdefg
0123456
1204365

If t is greater than 3(p-1) then the engine cannot prevent the player to win.
"""


class Engine:

    def __init__(self, nb_cards):
        self.nb_cards = nb_cards
        self.permutations = self.get_permutations()

    def get_permutations(self):
        permutation_1 = list(range(self.nb_cards))
        permutation_2 = [0] * self.nb_cards
        n = self.nb_cards - [0, 4, 2][self.nb_cards % 3]
        for i in range(0, n, 3):
            permutation_2[i:i + 3] = choice((permutation_1[i + 1:i + 3] + permutation_1[i:i + 1],
                                             permutation_1[i + 2:i + 3] + permutation_1[i:i + 2]))
        for i in range(n, self.nb_cards, 2):
            permutation_2[i:i + 2] = permutation_1[i + 1:i + 2] + permutation_1[i:i + 1]

        temp = list(zip(permutation_1, permutation_2))
        shuffle(temp)
        permutation_1, permutation_2 = zip(*temp)

        return tuple(permutation_1), tuple(permutation_2)

    def get_value(self, cards):
        while True:
            values = set(self.permutations[0][i] for i in cards)
            for p in self.permutations[1:]:
                values &= set(p[i] for i in cards)
            if not values:
                print("p is too low, we have to remove a permutation")
                self.permutations = self.permutations[:-1]
                continue
            return choice(list(values))

    def verify(self, card, value):
        return next((p for p in self.permutations if p[card] != value), self.permutations[0])


class Player(Protocol):
    def ask_cards(self) -> Optional[tuple[int, ...]]:
        ...

    def add_clue(self, cards, value):
        ...

    def guess_a_card(self) -> tuple[int, int]:
        ...


class RealPlayer(Player):

    def __init__(self, nb_cards, p):
        self.nb_cards = nb_cards
        self.p = p

    def ask_cards(self):
        while cards := cards_from_string(input("Cards: ")):
            if len(cards) != self.p:
                print(f"You have to enter {self.p} cards.")
                continue
            if max(cards) >= self.nb_cards:
                print(f"Card {cards_to_string((max(cards),))} is not in {cards_to_string(range(self.nb_cards))}.")
                continue
            return cards

    def add_clue(self, cards, value):
        print(f"Value: {value}")

    def guess_a_card(self):
        card, value = input("Guess a card: ").split()
        return cards_from_string(card)[0], int(value)


class SimulatedPlayer(Player):

    def __init__(self, nb_cards, p):
        self.nb_cards = nb_cards
        self.p = p
        self.clues = {}
        self.gen_ask_cards = self.find_card()
        self.prefixes = None

    def ask_cards(self) -> tuple[int, ...]:
        return next(self.gen_ask_cards, None)

    def add_clue(self, cards, value):
        print(f"{cards_to_string(cards)} -> {value}")
        self.clues[cards] = value

    def guess_a_card(self) -> tuple[int, int]:
        if answer := self.get_known_card():
            card, value = answer
            print(f"Guessing {cards_to_string((card,))} -> {value}.")
            return card, value

        print("Could not find a card. Possibilities of values are:")
        for prefix in self.prefixes:
            print(prefix)

        prefix = choice(self.prefixes)
        card = choice(range(len(prefix)))
        value = prefix[card]
        print(f"Guessing at random {cards_to_string((card,))} -> {value}.")

        return card, value

    def get_known_card(self) -> Optional[tuple[int, int]]:
        if not self.prefixes:
            return

        for card in range(len(self.prefixes[0])):
            values = set(prefix[card] for prefix in self.prefixes)
            if len(values) == 1:
                return card, values.pop()

    def find_card(self) -> Iterator[tuple[int, ...]]:
        cards = tuple(range(self.p))
        yield cards

        self.prefixes = tuple(p for p in permutations(range(self.nb_cards), self.p) if self.is_valid(p))

        for i in range(self.p, self.nb_cards):
            for cards in combinations(range(i), self.p - 1):
                yield cards + (i,)

            new_prefixes = []
            for value in range(self.nb_cards):
                for prefix in self.prefixes:
                    if value in prefix:
                        continue
                    prefix += (value,)
                    if self.is_valid(prefix):
                        new_prefixes.append(prefix)

            self.prefixes = new_prefixes
            if self.get_known_card():
                return

    def is_valid(self, prefix):
        return all(any(prefix[card] == value for card in cards)
                   for cards, value in self.clues.items())


class TheoreticalPlayer(Player):

    def __init__(self, nb_cards, p):
        self.nb_cards = nb_cards
        self.p = p
        self.clues = {}
        self.gen_ask_cards = self.find_card()
        self.valid_permutations = None

    def ask_cards(self) -> tuple[int, ...]:
        return next(self.gen_ask_cards, None)

    def add_clue(self, cards, value):
        print(f"{cards_to_string(cards)} -> {value}")
        self.clues[cards] = value

    def guess_a_card(self) -> tuple[int, int]:
        if answer := self.get_known_card():
            card, value = answer
            print(f"Guessing {cards_to_string((card,))} -> {value}.")
            return card, value

        print("Could not find a card. Possibilities of values are:")
        for permutation in self.valid_permutations:
            print(permutation)

        permutation = choice(list(self.valid_permutations))
        card = choice(range(len(permutation)))
        value = permutation[card]
        print(f"Guessing at random {cards_to_string((card,))} -> {value}.")

        return card, value

    def get_known_card(self) -> Optional[tuple[int, int]]:
        print(self.valid_permutations)
        if not self.valid_permutations:
            return

        for card in range(self.nb_cards):
            values = set(prefix[card] for prefix in self.valid_permutations)
            if len(values) == 1:
                return card, values.pop()

    def compute_cycles(self, permutation, permutation_):
        found_cards = set()
        cycles = []
        for card in range(self.nb_cards):
            if card in found_cards:
                continue
            cycle = []
            while not (cycle and card == cycle[0]):
                cycle.append(card)
                card = permutation_.index(permutation[card])
            cycles.append(cycle)
            found_cards |= set(cycle)
        return cycles

    def find_card(self):
        self.valid_permutations = set(permutations(range(self.nb_cards)))

        for permutation, permutation_ in combinations(self.valid_permutations, 2):
            if any(value == value_ for value, value_ in zip(permutation, permutation_)):
                continue

            cycles = self.compute_cycles(permutation, permutation_)

            cards = []
            for cycle in cycles:
                cards += cycle[:-1:2]
            for i in range(self.nb_cards):
                if len(cards) >= self.p:
                    break
                if i in cards:
                    continue
                cards.append(i)

            cards.sort()
            cards = tuple(cards[:self.p])

            if cards not in self.clues:
                yield cards

            value = self.clues[cards]
            if all(permutation[card] != value for card in cards):
                self.valid_permutations.discard(permutation)
            if all(permutation_[card] != value for card in cards):
                self.valid_permutations.discard(permutation_)


class NamiswanPlayer(Player):
    """Player from demonstration of Namiswan.

    See https://les-mathematiques.net/vanilla/index.php?p=/discussion/comment/2434285/#Comment_2434285
    """
    def __init__(self, nb_cards, p):
        self.nb_cards = nb_cards
        self.p = p
        self.clues = {}
        self.gen_ask_cards = self.ask_all_combinations()

    def ask_cards(self) -> Optional[tuple[int, ...]]:
        return next(self.gen_ask_cards, None)

    def add_clue(self, cards, value):
        print(f"{cards_to_string(cards)} -> {value}")
        self.clues[cards] = value

    def guess_a_card(self) -> tuple[int, int]:
        intersections = {}
        for cards, value in self.clues.items():
            if value in intersections:
                intersections[value] &= set(cards)
            else:
                intersections[value] = set(cards)

        for value, cards in intersections.items():
            if len(cards) == 1:
                card = cards.pop()
                print(f"Guessing {cards_to_string((card,))} -> {value}.")
                return card, value

        value = choice(list(intersections))
        card = choice(list(intersections[value]))
        print(f"Guessing at random {cards_to_string((card,))} -> {value}.")
        return card, value

    def ask_all_combinations(self):
        yield from combinations(range(self.nb_cards),  self.p)


def cards_to_string(cards):
    return ''.join(ascii_letters[c] for c in cards)


def cards_from_string(string):
    return tuple(ascii_letters.index(c) for c in string)


def main(nb_cards, p, player):
    print(f"Playing with {nb_cards} cards and with {p} cards asked each turn.")
    engine = Engine(nb_cards)
    player = player(nb_cards, p)

    while cards := player.ask_cards():
        player.add_clue(cards, engine.get_value(cards))

    card, value = player.guess_a_card()
    answer = engine.verify(card, value)

    if answer[card] == value:
        print(f"You found it! The values were {answer}.")
    else:
        print(f"Nice try but the values were {answer}.")


if __name__ == "__main__":
    main(nb_cards=10, p=4, player=NamiswanPlayer)
