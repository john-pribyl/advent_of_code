from enum import Enum, auto
from collections import defaultdict, deque
import copy
import heapq
import math
import time

# Important: Check UP, LEFT, RIGHT, then DOWN
DIRECTION_OFFSETS = [(-1,0), (0,-1), (0,1), (1,0)]

class PieceType(Enum):
    elf = auto()
    goblin = auto()

class GamePiece:
    def __init__(self, coordinates, piece_type):
        self.coordinates = coordinates
        self.piece_type = piece_type
        self.attack_power = 3
        self.hit_points = 200
    
    # Gets neighboring piece to attack or None if attack is not possible
    def get_piece_to_attack(self, board_state):
        piece_row, piece_col = self.coordinates
        neighboring_enemies = []
        for row_offset, col_offset in DIRECTION_OFFSETS:
            neighbor_coords = (piece_row + row_offset, piece_col + col_offset)
            if neighbor_coords in board_state:
                neighbor_piece = board_state[neighbor_coords]
                if neighbor_piece is not None and neighbor_piece.piece_type != self.piece_type:
                    neighboring_enemies.append(neighbor_piece)

        if len(neighboring_enemies) > 0:
            neighboring_enemies = sorted(
                neighboring_enemies,
                key=lambda enemy: (enemy.hit_points, enemy.coordinates)
            )
            return neighboring_enemies[0]
        else:
            return None
    
    def get_next_coords(self, board_state):
        # BFS to find nearest attack space
        # May be more than one at a given level, prioritize by coordinate
        queue = deque()
        queue.append((self.coordinates, 0, None)) # coordinates, distance, first_step
        max_distance = math.inf
        attack_space_heap = []
        seen = set()
        while len(queue) > 0:
            current_coords, current_distance, first_step = queue.popleft()
            # Check if we've been here
            if current_coords in seen:
                continue
            seen.add(current_coords)

            # Check if we're past max distance
            if current_distance > max_distance:
                break

            # Look at neighbors for path
            row_idx, col_idx = current_coords
            for row_offset, col_offset in DIRECTION_OFFSETS:
                neighbor_coords = (row_idx + row_offset, col_idx + col_offset)
                if neighbor_coords in board_state:
                    if board_state[neighbor_coords] is not None:
                        # Neighboring space is occupied, check for if it's an enemy
                        if board_state[neighbor_coords].piece_type != self.piece_type:
                            max_distance = current_distance
                            heapq.heappush(attack_space_heap, (first_step, current_coords))
                    else:
                        # Neighboring space is not occupied, visit it
                        path_start = neighbor_coords if not first_step else first_step
                        queue.append((neighbor_coords, current_distance + 1, path_start))

        if len(attack_space_heap) > 0:
            first_step, _ = heapq.heappop(attack_space_heap)
            return first_step
        else:              
            return None
    
    

def part1(initial_state, elf_attack_power = 3):
    initial_board_state, num_rows, num_cols = initial_state
    board_state = copy.deepcopy(initial_board_state)
    pieces = list(filter(lambda piece: piece is not None, board_state.values()))
    # For part 2, set elf attack power
    for piece in pieces:
        if piece.piece_type == PieceType.elf:
            piece.attack_power = elf_attack_power

    turn_idx = 1

    game_over = False
    elf_has_died = False # For part 2
    while not game_over:
        pieces = sorted(pieces, key=lambda piece: piece.coordinates)
        for piece in pieces:
            # Piece may have been killed by a neighbor already
            if piece.hit_points <= 0:
                continue 

            # Check for end of game by seeing if there are any opposing pieces remaining
            target_pieces = [
                other_piece for other_piece in pieces 
                if other_piece.piece_type != piece.piece_type and other_piece.hit_points > 0
            ]
            if not target_pieces:
                game_over = True
                break
            
            # Move piece
            next_coords = piece.get_next_coords(board_state)
            if next_coords:
                board_state[piece.coordinates] = None
                board_state[next_coords] = piece
                piece.coordinates = next_coords

            # See if piece can attack (has neighboring opposing piece)
            target_piece = piece.get_piece_to_attack(board_state)
            if target_piece:
                new_hitpoints = max(target_piece.hit_points - piece.attack_power, 0)
                target_piece.hit_points = new_hitpoints
                board_state[target_piece.coordinates].hit_points = new_hitpoints
                if target_piece.hit_points == 0:
                    board_state[target_piece.coordinates] = None
                    # Part 2, no elves are supposed to die
                    if target_piece.piece_type == PieceType.elf:
                        elf_has_died = True
                
        # After turn, remove dead pieces from board
        print_board_state(board_state, num_rows, num_cols, turn_idx)
        time.sleep(1)
        pieces = list(filter(lambda piece: piece.hit_points > 0, pieces))

        if not game_over:
            turn_idx += 1

    # print_board_state(board_state, num_rows, num_cols, turn_idx)
    pieces = list(filter(lambda piece: piece.hit_points > 0, pieces))
    sum_hitpoints = 0
    for piece in pieces:
        sum_hitpoints += piece.hit_points

    return (turn_idx - 1) * sum_hitpoints, elf_has_died

def part2(initial_board_state: defaultdict[(int, int), GamePiece]):
    board_state = copy.deepcopy(initial_board_state)
    elf_attack_power = 0
    elf_has_died = True
    while elf_has_died:
        elf_attack_power += 1
        result, elf_has_died = part1(board_state, elf_attack_power)

    return result

def parse_input(board):
    num_rows = len(board)
    num_cols = len(board[0].strip())
    board_state = defaultdict[(int, int), GamePiece]()
    for row_idx, row in enumerate(board):
        for col_idx, _ in enumerate(row):
            coordinates = (row_idx, col_idx)
            board_val = board[row_idx][col_idx]
            if board_val == "E":
                board_state[coordinates] = GamePiece(coordinates, PieceType.elf)
            elif board_val == "G":
                board_state[coordinates] = GamePiece(coordinates, PieceType.goblin)
            elif board_val == ".":
                board_state[coordinates] = None

    return board_state, num_rows, num_cols

def print_board_state(board_state, num_rows, num_cols, turn_idx):
    print(f"Turn: {turn_idx}")
    for row_idx in range(num_rows):
        row_string = ""
        for col_idx in range(num_cols):
            if (row_idx, col_idx) in board_state:
                if board_state[(row_idx, col_idx)] is None:
                    row_string += "."
                elif board_state[(row_idx, col_idx)].piece_type == PieceType.elf:
                    row_string += "E"
                elif board_state[(row_idx, col_idx)].piece_type == PieceType.goblin:
                    row_string += "G"
            else:
                row_string += "#"
        print(row_string)
    print("\n")

def main():
    example_input = open('./example.txt', 'r').read().strip().split('\n')
    parsed_example_state = parse_input(example_input)
    input = open('./input.txt', 'r').read().strip().split('\n')
    parsed_input_state = parse_input(input)

    # Part 1 Example
    part1_example_result, _ = part1(parsed_example_state)
    print(f"Part 1 (example): {part1_example_result}")

    # # Part 1
    # part1_result, _ = part1(parsed_input_state)
    # print(f"Part 1: {part1_result}")

    # # Part 2 Example
    # part2_example_result = part2(parsed_example_state)
    # print(f"Part 2 (example): {part2_example_result}")

    # # Part 2
    # part2_result = part2(parsed_input_state)
    # print(f"Part 2: {part2_result}")


main()