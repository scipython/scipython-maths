from df_maze import Maze

# Maze dimensions (ncols, nrows)
nx, ny = 15, 15
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.add_begin_end = True
maze.add_treasure = False
maze.make_maze()

print(maze)
maze.write_svg('maze3.svg')
maze.write_svg('maze3_solution.svg', solution=True)
print(maze.get_solution())
