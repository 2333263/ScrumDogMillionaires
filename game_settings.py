with open('Levels/level.txt') as f:
    lines = f.readlines()

level_array = lines
block_size = 48

width = int(block_size * len(level_array[0]))
height = int(block_size * len(level_array))

