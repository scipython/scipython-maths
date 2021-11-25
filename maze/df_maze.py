# df_maze.py
import random

import numpy as np


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

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

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

    def write_svg(self, filename, start=(), end=()):
        """Write an SVG image of the maze to filename.

        if the optional 'end' parameter (end=(x,y)) is supplied,
        the maze will be solved from the 'start' (default value:
        entry position) to the 'end' position and will be indicated
        in the SVG image.
        """

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

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
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

            # VISUALIZE THE MAZE SOLUTION (if demanded) ### begin #
            # If the write_svg method is called with the "end" parameter
            # specified, then solve the maze using the cellular automata
            # approach and include it in the output SVG image.
            if end:
                # The end cell is included in the call, so solve the maze
                if not start:
                    # Starting cell is not specified, so use the initial designation
                    start = (self.ix, self.iy)

                # Solve the maze:
                solution = self.solve_from_to(start, end)
                for i in range(np.size(solution, 0) - 1):
                    x1, y1 = solution[i, :]
                    x2, y2 = solution[i + 1, :]
                    x1, y1, x2, y2 = (x1 + 0.5) * scx, (y1 + 0.5) * scy, (x2 + 0.5) * scx, (y2 + 0.5) * scy
                    print('<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:#7d8059;" />'
                          .format(x1, y1, x2, y2), file=f)
            # VISUALIZE THE MAZE SOLUTION (if demanded) ### end #

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            print('</svg>', file=f)

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

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
            nv += 1

    def solve_from_to(self, start, end):
        """Solves the path from start = (x0,y0) to end = (x1,y1)
        using cellular automata.

        Returns the steps' coordinates
        """

        # Check that the start & end parameters are within boundaries:
        np_start = np.array(start)
        np_end = np.array(end)
        np_start[np_start < 0] = 0
        if np_start[0] >= self.nx:
            np_start[0] = self.nx - 1
        if np_start[1] >= self.ny:
            np_start[1] = self.ny - 1

        np_end[np_end < 0] = 0
        if np_end[0] >= self.nx:
            np_end[0] = self.nx - 1
        if np_end[1] >= self.ny:
            np_end[1] = self.ny - 1

        x0 = np_start[0]
        y0 = np_start[1]
        x1 = np_end[0]
        y1 = np_end[1]

        # Initially set the states of all cells to "O" for Open
        arr_states = np.full((self.nx, self.ny), "O", dtype=str)
        arr_states[x0, y0] = 'S'  # Designates Start
        arr_states[x1, y1] = 'E'  # Designates End

        # Defining a canvas to apply the filter
        # for our playground
        canvas = np.empty((self.nx, self.ny), dtype=object)
        for x in range(self.nx):
            for y in range(self.ny):
                canvas[x, y] = (x, y)

        state2logic = {"S": False, "E": False, "O": False, "X": True}
        neigh2state = ["O", "O", "O", "X"]
        # Pick the "open" states as they are the ones whose states can change:
        filt = arr_states == "O"
        num_Os = np.sum(filt)

        # We will continue our investigation, closing those cells
        # that are in contact with three closed cells+walls (meaning
        # that, it is a dead end itself) at each iteration. Mind that,
        # it is an _online_ process where the next cell is checked
        # against the already updated states of the cells coming before
        # it (as opposed to the _batch_ process approach)
        #
        # The iteration is continued until no cell has changed its
        # status, meaning that we have arrived at a solution.
        num_Os_pre = num_Os + 1
        while num_Os != num_Os_pre:
            num_Os_pre = num_Os
            for xy in canvas[filt]:
                num_Os_pre = num_Os
                x, y = xy
                walls = np.array(list(self.cell_at(x, y).walls.values()))

                # N-S-E-W
                neighbours = np.array([True, True, True, True])
                # We are using try..except to ensure the neighbours
                # exist (considering the boundaries)
                # (for the purpose here, they are much "cheaper" than
                # if clauses)
                try:
                    neighbours[0] = state2logic[arr_states[x, y - 1]]
                except:
                    pass
                try:
                    neighbours[1] = state2logic[arr_states[x, y + 1]]
                except:
                    pass
                try:
                    neighbours[2] = state2logic[arr_states[x + 1, y]]
                except:
                    pass
                try:
                    neighbours[3] = state2logic[arr_states[x - 1, y]]
                except:
                    pass
                # Being bounded by a wall at a specific direction
                # or having a closed neighbour there are equivalent
                # in action and if the total number of such directions
                # is 3 (i.e., 1 entrance, no exit), then the cell is
                # closed.
                res = np.logical_or(walls, neighbours)
                arr_states[x, y] = neigh2state[np.sum(res)]
            # For the next iteration, focus only on the still Open ones
            # (This also causes the process to get faster as it proceeds)
            filt = arr_states == "O"
            num_Os = np.sum(filt)

        # Now we have the canvas containing the path,
        # starting from "S", followed by "O"s up to "E"
        pos_start = canvas[arr_states == "S"][0]
        path_line = np.array([pos_start])
        pos_end = canvas[arr_states == "E"][0]
        pos = pos_start
        pos_pre = (-1, -1)
        step = 0
        # Define a control (filled with -1) array to keep track of visited cells
        arr_path = np.ones((self.nx, self.ny)) * -1
        arr_path[pos_start[0], pos_start[1]] = 0
        arr_path[pos_end[0], pos_end[1]] = "999999"
        directions = np.array(["N", "S", "E", "W"])
        while pos != pos_pre:
            pos_pre = pos
            step += 1
            possible_ways = np.array(list(self.cell_at(pos[0], pos[1]).walls.values())) == False
            delta = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
            for direction in directions[possible_ways]:
                # pick this direction if it is open and not visited before
                if (arr_states[pos[0] + delta[direction][0], pos[1] + delta[direction][1]] == "O" and arr_path[
                       pos[0] + delta[direction][0], pos[1] + delta[direction][1]] == -1):
                    arr_path[pos[0] + delta[direction][0], pos[1] + delta[direction][1]] = step
                    pos = (pos[0] + delta[direction][0], pos[1] + delta[direction][1])
                    path_line = np.append(path_line, [pos], axis=0)
                    break
        # Even though being an auxiliary and internal variable, if needed,
        # arr_path contains the steps at which the corresponding cell is visited,
        # thus paving the way to the exit.
        arr_path[pos_end[0], pos_end[1]] = step
        path_line = np.append(path_line, [pos_end], axis=0)
        return path_line
