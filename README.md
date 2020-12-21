<h1 align="center">
  <b>A* Path Finding Visualization in Python</b>
</h1>

<p align="center">
  <img src="https://media.giphy.com/media/CLAozFfuhi9nFnZ0VR/giphy.gif" alt="animated" />
</p>

This A* Path Finding visualizer writting in Python 3 is designed with pygame and uses the manhattan distance for calculating the heuristic.
Therefore, A* is guaranteed to find a shortest path. Other heuristic methods have proven better but manhattan distance is very simple which is why I used it.
A big thanks to Tech With Tim for the video and the inspiration to do this project

## Requirements
Visit [requirements.txt file](requirements.txt)
After cloning the repository, to install the requirements easily run the following command
```
pip install -r requirements.txt
```
Or depending on your operating system, you might have to run 
```
pip3 install -r requirements.txt
```

## How to run
After installing the necessary requirements listed in requirements.txt, run the following command
```
python path.py
```
Or depending on your operating system, you might have to run
```
python3 path.py
```

## How to use the program
- After running the command found in the 'How to run' section above, a pygame window will appear
- Your first click will be the start node and your second click will be the end node
- These two nodes are specified by their color
- Start = blue
- End = purple
- Any other left click after the first two clicks, renders a wall on the grid (a node in which A* will not consider)
- If you made a mistake or want to clear a node, you simply right click on the node

- To start A* path finder, simply press the space bar
- To reset the grid, simply press backspace
