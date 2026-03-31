from collections import deque
import time

class CardDeck:
    def __init__(self, card_count):
        self.card_count = card_count
        self.cards = deque([val for val in range(card_count)])
        self.direction = 1
    
    def list_cards(self):
        start_idx = 0
        end_idx = self.card_count
        if self.direction == -1:
            start_idx += 1
            end_idx += 1
        return [self.cards[idx * self.direction] for idx in range(start_idx, end_idx)]
    
    def locate_card(self, card_value):
        start_idx = 0
        end_idx = self.card_count
        if self.direction == -1:
            start_idx += 1
            end_idx += 1
        for idx in range(start_idx, end_idx):
            if self.cards[idx * self.direction] == card_value:
                return idx

    def reverse_deck(self):
        self.direction *= -1

    def cut_deck(self, offset):
        self.cards.rotate(offset * -self.direction)

    def deal_deck(self, increment):
        new_deck = [0] * self.card_count
        for idx in range(self.card_count):
            source_idx = idx
            if self.direction == -1:
                source_idx = -(idx + 1)
            destination_idx = idx * increment % self.card_count
            new_deck[destination_idx] = self.cards[source_idx]
        self.cards = deque(new_deck)
        self.direction = 1

def part1(input, card_count, card_to_locate):
    card_deck = CardDeck(card_count)

    for line in input:
        line_parts = line.strip().split()
        if line_parts[0] == "cut":
            card_deck.cut_deck(int(line_parts[1]))
        elif line_parts[0] == "deal" and line_parts[1] == "into":
            card_deck.reverse_deck()
        elif line_parts[0] == "deal" and line_parts[1] == "with":
            card_deck.deal_deck(int(line_parts[3]))
        else:
            print("unmatched input")

    # print(card_deck.list_cards())
    return card_deck.locate_card(card_to_locate)


def part2(input, card_count, card_to_locate, num_repitions):
    card_idx = card_to_locate

    for _ in range(num_repitions):
        for line in input:
            line_parts = line.strip().split()
            if line_parts[0] == "cut":
                cut_idx = int(line_parts[1])
                # Adjust negative cuts to positive cuts
                if cut_idx < 0:
                    cut_idx = card_count + cut_idx
                
                if card_idx >= cut_idx:
                    card_idx -= cut_idx
                else:
                    card_idx = card_count - (cut_idx - card_idx)
            elif line_parts[0] == "deal" and line_parts[1] == "into":
                card_idx = (card_count - 1) - card_idx
            elif line_parts[0] == "deal" and line_parts[1] == "with":
                increment = int(line_parts[3])
                card_idx = card_idx * increment % card_count
            else:
                print("unmatched input")

    return card_idx

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result = part1(example_input, 10, 7)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input, 10007, 2019)
    print(f"Part 1: {part1_result}")

    # Part 1 (Improved)
    part1_improved_result = part2(input, 10007, 2019, 100_000)
    print(f"Part 1 (improved): {part1_improved_result}")

    # Part 2 done in Rust    

main()