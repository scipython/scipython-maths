The script `df_maze.py` creates a maze using the depth-first algorithm as described at https://scipython.com/blog/making-a-maze/.
Change the dimensions by altering the variables `nx` and `ny`.

For example with `nx = ny = 40`:

<p align="center">
<img width="515" height="515" src="df_maze.png" alt="Sample depth-first 40x40 maze">
</p>

`ca_maze.py` creates the frames for an animation of the growth of a maze using the cellular automaton algorithm described at https://scipython.com/blog/maze-generation-by-cellular-automaton/. The frames are written to the subdirectory `ca_frames/` and the maze size is again set by the variables `nx` and `ny`. The frames can be put together into an animated gif with [Imagemagick](https://www.imagemagick.org/script/index.php)'s `convert` utility. For example:

<p align="center">
<img width="600" height="450" src="ca_maze1.gif" alt="Sample cellular automaton maze generation">
</p>
