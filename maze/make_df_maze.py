from df_maze import Maze

# Maze dimensions (ncols, nrows)
nx, ny = 15, 15
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.make_maze()

print(maze)
maze.write_svg('maze.svg')

# Solve the maze from the entry position to (13,12)
# solution_path = maze.solve_from_to((ix,iy),(13,12))
# print(solution_path)

# Draw the solution from the entry position to (10,5)
maze.write_svg('maze_solved.svg', end=(10, 5))
