import random

def generate_maze(width, height):
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    maze = [[1 for _ in range(width)] for _ in range(height)]
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]  # Right, Left, Down, Up

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    maze[0][1] = 0  # Entrance
    maze[height - 1][width - 2] = 0  # Exit

    return maze, (1, 0), (width - 2, height - 1)



def solve_maze(maze, start, end):
    """
    Solves a maze using depth-first search (DFS) and tracks the path.

    Args:
        maze: A 2D list representing the maze, where 0 is a path and 1 is a wall.
        start: A tuple (x, y) representing the starting position.
        end: A tuple (x, y) representing the ending position.

    Returns:
        path: A list of tuples representing the path from start to end if one exists.
        explored: A list of tuples representing all explored positions.
    """
    width = len(maze[0])  # Maze dimensions
    height = len(maze)
    stack = [start]
    visited = [[False for _ in range(width)] for _ in range(height)]
    parent = [[None for _ in range(width)] for _ in range(height)]
    explored = []

    visited[start[1]][start[0]] = True
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    while stack:
        current = stack[-1]
        x, y = current
        explored.append(current)

        # Debugging information
        # print(f"Current position: {current}")
        # print(f"Stack state: {stack}")

        if current == end:
            print("End reached!")
            break

        moved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < width
                and 0 <= ny < height
                and maze[ny][nx] == 0
                and not visited[ny][nx]
            ):
                stack.append((nx, ny))
                visited[ny][nx] = True
                parent[ny][nx] = (x, y)
                moved = True
                break

        if not moved:
            stack.pop()

    # Backtrack to reconstruct the path
    path = []
    if current == end:
        while current != start:
            path.append(current)
            current = parent[current[1]][current[0]]
        path.append(start)
        path.reverse()

    return path, explored



def save_maze_to_ppm(maze, filename, path=None, explored=None):
    height = len(maze)
    width = len(maze[0])

    with open(filename, 'w') as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for y in range(height):
            for x in range(width):
                if path and (x, y) in path:
                    f.write("255 105 180 ")  # Pink = solution path
                elif explored and (x, y) in explored:
                    f.write("255 255 0 ")  # Yellow = explored paths
                elif maze[y][x] == 1:
                    f.write("0 0 0 ")  # Wall = black
                else:
                    f.write("255 255 255 ")  # Path = white
            f.write("\n")

if __name__ == "__main__":
    grid_width = int(input("Enter the grid width: "))
    grid_height = int(input("Enter the grid height: "))
    
    maze, start, end = generate_maze(grid_width, grid_height)
    save_maze_to_ppm(maze, "maze.ppm")  # Save the initial maze without shortest path
    print("Maze saved to 'maze.ppm'")

    # Ask user if they want to solve the maze
    save_solution = input("Do you want to save the solved maze with the shortest path? (Y/N): ").strip().upper()
    
    if save_solution == 'Y':
        path, explored = solve_maze(maze, start, end)
        if path:
            save_maze_to_ppm(maze, "mazeSolved.ppm", path)
            print("Solved maze saved to 'mazeSolved.ppm'")
        else:
            print("No solution found!")

    # initially for debugging purposes but kept
    # Always save the paths explored, regardless of whether a solution is found
    save_maze_to_ppm(maze, "PathsExplored.ppm", explored=explored)
    print("Paths explored saved to 'PathsExplored.ppm'")

