# df_maze.py
import random


# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.

class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    # A mapping of cardinal directions to coordinate differences.
    delta = {'W': (-1, 0), 'E': (1, 0), 'S': (0, 1), 'N': (0, -1)}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
    
    def __repr__(self):
        """return a string representation of a cell"""
        return f'({self.x}, {self.y})'

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

        self.add_begin_end = False
        self.add_treasure = False
        self.treasure_x = random.randint(0, self.nx-1)
        self.treasure_y = random.randint(0, self.ny-1)

        # Give the coordinates of walls that you do *not* wish to be
        # present in the output here.
        self.excluded_walls = [((nx-1, ny), (nx, ny)),
                               ((0, 0), (0, 1))]
        
        # Store the solution to the maze
        self.solution = None

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]


    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)


    def write_svg(self, filename, solution=False):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(f, x1, y1, x2, y2):
            """Write a single wall to the SVG image file handle f."""

            if ((x1, y1), (x2, y2)) in self.excluded_walls:
                print(f'Excluding wall at {((x1, y1), (x2, y2))}')
                return
            sx1, sy1, sx2, sy2 = x1*scx, y1*scy, x2*scx, y2*scy
            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(sx1, sy1, sx2, sy2), file=f)

        def add_cell_rect(f, x, y, colour):
            pad = 5
            print(f'<rect x="{scx*x+pad}" y="{scy*y+pad}" width="{scx-2*pad}"'
                  f' height="{scy-2*pad}" style="fill:{colour}" />', file=f) 

        def add_path_segment(f, cell, next_cell):
            sx1, sy1 = scx * (cell.x + 0.5), scy * (cell.y + 0.5)
            sx2, sy2 = scx * (next_cell.x + 0.5), scy * (next_cell.y + 0.5)
            print(f'<line x1="{sx1}" y1="{sy1}" x2="{sx2}" y2="{sy2}" style="stroke:rgb(0,0,255)" />',
                  file=f)

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x, y+1, x+1, y+1
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = x+1, y, x+1, y+1
                        write_wall(f, x1, y1, x2, y2)

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            for x in range(self.nx):
                write_wall(f, x, 0, x+1, 0)
            for y in range(self.ny):
                write_wall(f, 0, y, 0, y+1)
                
            #print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            #print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)

            if self.add_begin_end:
                add_cell_rect(f, 0, 0, 'green')
                add_cell_rect(f, self.nx - 1, self.ny - 1, 'red')
            if self.add_treasure:
                add_cell_rect(f, self.treasure_x, self.treasure_y, 'yellow')

            if solution:
                if self.solution is None:
                    print('Error:  There is no solution stored.')
                else:
                    for i, cell in enumerate(self.solution[:-1]):
                        next_cell = self.solution[i+1]
                        add_path_segment(f, cell, next_cell)

            print('</svg>', file=f)


    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        neighbours = []
        for direction, (dx, dy) in Cell.delta.items():
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours


    def get_solution(self):
        return self.solution


    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            
            # Store the solution if we are at the exit cell
            if (current_cell.x == self.nx - 1) and \
               (current_cell.y == self.ny - 1):
                self.solution = cell_stack.copy()
                self.solution.append(next_cell)
            nv += 1
