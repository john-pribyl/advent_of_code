from collections import deque

class ListNode:
    def __init__(self, val, previous_node=None, next_node=None):
        self.val = val
        self.previous_node = previous_node if previous_node else self
        self.next_node = next_node if next_node else self

# Does part 1 and 2
def part1(input, round_multiplier=1):
    last_line = input[-1]
    round_result = 0
    num_players, num_marbles = parse_line(last_line)
    num_marbles *= round_multiplier
    round_result = play_round_deque(num_players, num_marbles)
    return round_result

def play_round(num_players, num_marbles):
    # Initialize player scores
    player_scores = {}
    for idx in range(num_players):
        player_scores[idx] = 0

    # Initialize marbles as a doubly linked list
    list_head = ListNode(0)
    current_node = list_head
    current_player_idx = 0
    for turn_idx in range(1, num_marbles + 1):
        if turn_idx % 23 != 0:
            # Move 1 node clockwise
            current_node = current_node.next_node
            # Get reference to following node
            following_node = current_node.next_node

            # Insert new node between current node and next node
            node_to_insert = ListNode(turn_idx, current_node, following_node)
            current_node.next_node = node_to_insert
            following_node.previous_node = node_to_insert

            # Move to newly inserted node
            current_node = node_to_insert
        else:
            # Move seven nodes counterclockwise
            for _ in range(7):
                current_node = current_node.previous_node

            # Add node val and node that was to be placed to player score
            player_scores[current_player_idx] += turn_idx + current_node.val

            # Remove node at position
            current_node.previous_node.next_node = current_node.next_node
            current_node.next_node.previous_node = current_node.previous_node

            # Move 1 node clockwise
            current_node = current_node.next_node

        # Move to next player
        current_player_idx = (current_player_idx + 1) % num_players

    # Return high score
    return max(player_scores.values())

def play_round_deque(num_players, num_marbles):
    # Initialize player scores
    player_scores = {}
    for idx in range(num_players):
        player_scores[idx] = 0

    # Deques are circular doubly-linked lists.
    marble_cirle = deque()
    marble_cirle.append(0)
    current_player_idx = 0
    for marble_idx in range(1, num_marbles + 1):
        if marble_idx % 23 != 0:
            marble_cirle.rotate(1)
            marble_cirle.append(marble_idx)
            marble_cirle.rotate(1)
        else:
            marble_cirle.rotate(-8)
            player_scores[current_player_idx] += marble_cirle.pop() + marble_idx
            marble_cirle.rotate(1)

        current_player_idx = (current_player_idx + 1) % num_players

    return max(player_scores.values())


def parse_line(line):
    line_parts = line.split()
    return int(line_parts[0]), int(line_parts[6])

def main():
    example_input = open('./example.txt', 'r').read().strip().split('\n')
    input = open('./input.txt', 'r').read().strip().split('\n')

    # Part 1 Example (37305)
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1 (412959)
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example (320997431)
    part1_example_result = part1(example_input, 100)
    print(f"Part 2 (example): {part1_example_result}")

    # Part 2 (3333662986)
    part1_result = part1(input, 100)
    print(f"Part 2: {part1_result}")


main()