import math
import time

class Particle:
    def __init__(self, position_tuple, velocity_tuple):
        self.position = position_tuple
        self.velocity = velocity_tuple

# Does part 1 and 2
def part1(input):

    iteration = 0
    last_x_variance = math.inf
    while True:
        # Calculate position of each particle in this tick
        max_x, min_x, max_y, min_y = -math.inf, math.inf, -math.inf, math.inf
        this_round_particles = set()
        for particle in input:
            initial_position_x, initial_position_y = particle.position
            velocity_x, velocity_y = particle.velocity

            # Calculate particle's current position
            current_position_x = initial_position_x + (velocity_x * iteration)
            current_position_y = initial_position_y + (velocity_y * iteration)

            # Check if boundary needs to expand
            max_x, min_x = max(max_x, current_position_x), min(min_x, current_position_x)
            max_y, min_y = max(max_y, current_position_y), min(min_y, current_position_y)

            this_round_particles.add((current_position_x, current_position_y))

        print(f"Iteration: {iteration}")
        # Check if particles are getting further apart
        this_x_variance = abs(max_x - min_x)
        if this_x_variance > last_x_variance:
            break

        last_x_variance = this_x_variance

        # Check if particles are pretty close together
        if this_x_variance > 50:
            iteration += 1
            continue

        # Print drawing
        drawing = ["".join("#" if (x, y) in this_round_particles else "." for y in range(min_y, max_y + 1)) for x in range(min_x, max_x + 1)]
        for line in drawing:
            print(line)
        print('\n')

        time.sleep(1)
    
        iteration += 1

def parse_input(input):
    result = []
    for line in input:
        position_part, velocity_part = line.split(" velocity=<")
        position_part = position_part.split("<")[1][:-1]
        position_y, position_x = position_part.split(",")
        position_x = int(position_x.strip())
        position_y = int(position_y.strip())

        velocity_part = velocity_part[:-1]
        velocity_y, velocity_x = velocity_part.split(",")
        velocity_x = int(velocity_x.strip())
        velocity_y = int(velocity_y.strip())

        result.append(Particle((position_x, position_y), (velocity_x, velocity_y)))

    return result

def main():
    example_input = open('./example.txt', 'r').read().strip().split('\n')
    parsed_example_input = parse_input(example_input)
    input = open('./input.txt', 'r').read().strip().split('\n')
    parsed_input  = parse_input(input)

    # Part 1 & 2 Example
    # part1(parsed_example_input)

    # Part 1 & 2
    part1(parsed_input)

main()