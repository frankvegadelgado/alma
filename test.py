################################################################

import random

def generate_bipartite_graph(k):
  """
  Generates a random bipartite graph with at least k vertices on each side.

  Args:
      k: Minimum number of vertices on each side of the bipartition.

  Returns:
      An adjacency list representation of the bipartite graph.
  """
  graph = {i: [] for i in range(2*k)}  # Initialize empty adjacency list

  # Add edges between random vertices in each set
  for _ in range(k * 2):
    left_vertex = random.randint(0, k-1)
    right_vertex = random.randint(k, 2*k-1)
    graph[left_vertex].append(right_vertex)
    graph[right_vertex].append(left_vertex)

  return graph

# Example usage
k = 3
graph = generate_bipartite_graph(k)

# Print the adjacency list representation of the graph
print(graph)


#############################################################

from collections import deque

def is_bipartite(graph):
  colors = {}  # Dictionary to store node colors (red or blue)
  queue = deque()

  # Start BFS traversal from an arbitrary node
  for node in graph:
    if node not in colors:
      queue.append(node)
      colors[node] = "red"  # Assign initial color (red)

      while queue:
        current_node = queue.popleft()
        current_color = colors[current_node]

        # Explore uncolored neighbors
        for neighbor in graph[current_node]:
          if neighbor not in colors:
            queue.append(neighbor)
            colors[neighbor] = "blue" if current_color == "red" else "red"
          # If neighbor is already colored and same as current, graph is not bipartite
          elif colors[neighbor] == current_color:
            return None  # Not bipartite

  return colors

# Example usage
#graph = {
#  0: [1, 2],
#  1: [2, 3],
#  2: [0, 3, 4],
#  3: [1, 4],
#  4: [2]
#}

coloring = is_bipartite(graph)

if coloring is None:
  print("The graph is not bipartite")
else:
  print("Valid Bipartite Coloring:")
  for node, color in coloring.items():
    print(f"Node {node}: {color}")
