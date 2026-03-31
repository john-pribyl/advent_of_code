def part1(num_recipes):
    recipes = "37"
    elf1_idx = 0
    elf2_idx = 1

    while len(recipes) < num_recipes + 10:
        # Build new recipe score
        new_recipe_score = int(recipes[elf1_idx]) + int(recipes[elf2_idx])
        recipes += str(new_recipe_score)

        # Move elves
        elf1_idx = (elf1_idx + int(recipes[elf1_idx]) + 1) % len(recipes)
        elf2_idx = (elf2_idx + int(recipes[elf2_idx]) + 1) % len(recipes)

    return recipes[num_recipes:num_recipes + 10]

def part2(target_val):
    target_array = [int(char) for char in str(target_val)]
    target_length = len(target_array)
    recipes = [3, 7]
    elf1_idx = 0
    elf2_idx = 1
    sliding_window = 37

    while True:
        new_recipe_score = recipes[elf1_idx] + recipes[elf2_idx]

        for digit in (new_recipe_score // 10, new_recipe_score % 10) if new_recipe_score >= 10 else (new_recipe_score,):
            recipes.append(digit)
            sliding_window = (sliding_window * 10 + digit) % (10 ** target_length)
            
            if sliding_window == target_val:
                return len(recipes) - target_length


        elf1_idx = (elf1_idx + int(recipes[elf1_idx]) + 1) % len(recipes)
        elf2_idx = (elf2_idx + int(recipes[elf2_idx]) + 1) % len(recipes)
        
        


def main():
    # Part 1 (example)
    part1_example_result = part1(2018)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(157901)
    print(f"Part 1: {part1_result}")

    # Part 2 (example)
    part2_example_result = part2(59414)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_result = part2(157901)
    print(f"Part 2: {part2_result}")

main()