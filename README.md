<picture>
  <source media="(prefers-color-scheme: light)" srcset="/.github/meta/dark.png">
  <source media="(prefers-color-scheme: dark)" srcset="/.github/meta/light.png">
  <img alt="Voronoi Diagram Visualizer">
</picture>

## 📖 About

An interactive Python implementation of Voronoi diagrams using Fortune's sweep line algorithm. This educational tool provides real-time visualization of the algorithm's execution with support for interactive site manipulation, Delaunay triangulation display, and largest empty circle computation.

## 🌟 Features

### Core Algorithm
- **Fortune's Sweep Line Algorithm**: Efficient O(n log n) implementation
- **Real-time Execution**: Watch the algorithm progress with animated sweep line
- **Beachline Visualization**: See parabolic arcs forming and evolving
- **Event Processing**: Visual representation of site and circle events

### Interactive Controls
- **Site Management**: Click to add sites, right-click to remove
- **Dynamic Editing**: Drag sites to see real-time diagram updates
- **Zoom & Pan**: Navigate large diagrams with precision controls
- **Speed Control**: Adjust sweep line animation speed

### Advanced Features
- **Delaunay Triangulation**: Toggle dual graph visualization
- **Largest Empty Circle**: Find and display the maximum empty circle
- **Custom Point Sets**: Load points from external files
- **High Precision**: Uses NumPy float64 for numerical stability

## 🚀 Quick Start

### Prerequisites
```bash
pip install pygame numpy
```

### Running the Application
```bash
python main.py
```

### Basic Usage
1. **Add Sites**: Left-click anywhere to place a new site
2. **Start Algorithm**: Press `K` to begin sweep line animation
3. **Interactive Mode**: Drag sites to see immediate updates
4. **Help**: Press `H` for complete control reference

## 🎮 Controls Reference

| Key/Action      | Function                            |
|-----------------|-------------------------------------|
| **Left Click**  | Add new site or select existing     |
| **Right Click** | Remove site                         |
| **Drag Mouse**  | Move selected site                  |
| **W, A, S, D**  | Pan diagram view                    |
| **I / O**       | Zoom in / out                       |
| **K**           | Start/pause sweep line animation    |
| **J / L**       | Decrease/increase animation speed   |
| **M**           | Toggle largest empty circle display |
| **N**           | Toggle Delaunay triangulation       |
| **E**           | Redraw diagram                      |
| **R**           | Clear all sites                     |
| **H**           | Show/hide help                      |
| **Q**           | Quit application                    |

### Running as an API (No GUI)
You can run the application in API mode to process Voronoi diagrams interactively via commands.

#### Protocol Mode

Start protocol mode:
```bash
python main.py --no-gui
```

You will be prompted for commands. Each command is processed immediately or upon `RUN`. Type `EXIT` to quit.

#### Supported Commands

| Command                       | Description                                      |
|-------------------------------|--------------------------------------------------|
| `ADD (x, y)`                  | Add a site at coordinates (x, y)                 |
| `REMOVE (x, y)`               | Remove a site at coordinates (x, y)              |
| `PAN X <dx>`                  | Pan X by `<dx>` units                            |
| `PAN Y <dy>`                  | Pan Y by `<dy>` units                            |
| `ZOOM <factor>`               | Set zoom factor                                  |
| `DELAUNAY ON` / `OFF`         | Enable/disable Delaunay triangulation output     |
| `LEC ON` / `OFF`              | Enable/disable largest empty circle output       |
| `EVENTS ON` / `OFF`           | Enable/disable next event output                 |
| `SWEEPLINE ON` / `OFF`        | Enable/disable sweepline y-value output          |
| `RUN`                         | Compute and print the current diagram            |
| `CLEAR`                       | Remove all sites                                 |
| `EXIT`                        | Quit protocol mode                               |

#### Example Session

```
$ python main.py --no-gui
Voronoi API protocol mode. Type commands (EXIT to quit).
> ADD (100, 100)
Added site (100.0, 100.0)
> ADD (200, 150)
Added site (200.0, 150.0)
> DELAUNAY ON
Delaunay output enabled
> RUN
Voronoi Edges:
(100.0, 100.0) -> (200.0, 150.0)
...
Delaunay Triangulation Edges:
(100.0, 100.0) -> (200.0, 150.0)
...
> EXIT
```

## 📁 Project Structure

```
voronoi/
├── main.py              # Application entry point
├── gui.py               # PyGame-based user interface
├── constants.py         # Configuration and styling
├── points.txt           # Default point set
├── algorithm/
│   ├── voronoi.py       # Main algorithm implementation
│   ├── beachline.py     # Beachline data structure
│   └── event.py         # Site and circle events
├── geometry/
│   ├── point.py         # 2D point operations
│   ├── arc.py           # Parabolic arc representation
│   └── edge.py          # Voronoi edge handling
├── structures/
│   ├── tree.py          # AVL tree for beachline
│   └── list.py          # Doubly linked list
└── fonts/               # Custom typography
```

## 🧮 Algorithm Details

### Fortune's Sweep Line Algorithm
The implementation follows Fortune's classical approach:

1. **Site Events**: Process sites in y-coordinate order
2. **Beachline Maintenance**: Use AVL tree for efficient arc lookup
3. **Circle Events**: Detect and handle arc disappearances
4. **Edge Construction**: Build Voronoi edges incrementally

### Data Structures
- **AVL Tree**: Self-balancing binary search tree for O(log n) beachline queries
- **Doubly Linked List**: Maintains beachline arc sequence
- **Priority Queue**: Manages event processing order
- **High-Precision Arithmetic**: NumPy float64 for numerical stability

### Geometric Computations
- **Parabola Intersection**: Analytical solution for arc boundaries
- **Circle Events**: Three-point circumcircle calculations with degeneracy handling
- **Edge Extensions**: Proper boundary clipping for finite diagram display

## 📊 Input Format

### Point File (`points.txt`)
Define points as Python tuples, one per line:
```
(100, 100)
(200, 150)
(150, 200)
```

### Coordinate System
- **Range**: (-512, -512) to (512, 512)
- **Origin**: Center of display window
- **Y-Axis**: Standard mathematical orientation (up is positive)

## 🔧 Customization

### Visual Styling
Modify `constants.py` to customize:
- Colors and themes
- Animation speeds
- Zoom levels
- Site and edge styling

### Algorithm Parameters
Adjust precision and performance settings:
```python
EPSILON = 1e-6          # Numerical precision threshold
WIDTH = 1024            # Display dimensions
HEIGHT = 1024
```

## 🎓 Educational Use

This implementation is designed for learning and teaching computational geometry:

### Key Concepts Demonstrated
- **Sweep Line Paradigm**: Event-driven geometric algorithms
- **Duality**: Voronoi diagrams ↔ Delaunay triangulations
- **Data Structure Design**: Specialized structures for geometric queries
- **Numerical Robustness**: Handling floating-point precision issues

### Visualization Benefits
- **Step-by-step Execution**: Observe algorithm state changes
- **Interactive Exploration**: Experiment with different point configurations
- **Geometric Intuition**: Visual understanding of mathematical concepts

## 🐛 Troubleshooting

### Common Issues
- **Font Loading Errors**: Fallback fonts are automatically selected
- **Performance**: Reduce animation speed for complex diagrams
- **Precision**: Increase `EPSILON` if experiencing numerical instability

### Debug Mode
Run with verbose output:
```bash
python -u main.py
```

## ⚖️ License

This repository is licensed under the [MIT License](License).

With this license, you are allowed to:
- Use, copy, modify, and distribute the software
- Create derivative works and commercial applications
- Include the software in larger projects
- Redistribute under the same or different license terms

However, please respect academic integrity if using this for educational purposes and do not submit the code as your own original work without proper attribution.

## 📚 References

- O'Rourke, Joseph. *Computational Geometry in C*. Cambridge University Press, 1998.
- de Berg, Mark, et al. *Computational Geometry: Algorithms and Applications*. Springer, 2008.
- [Fortune's Algorithm - Jacques Heunis](https://jacquesheunis.com/post/fortunes-algorithm/)
- [Fortune's Algorithm Implementation - Jacques Heunis](https://jacquesheunis.com/post/fortunes-algorithm-implementation/)
- [Fortune Algorithm Details - Pierre Vigier](https://pvigier.github.io/2018/11/18/fortune-algorithm-details.html)

