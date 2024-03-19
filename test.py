def has_independent_vertex_cover_of_size_k(graph, k):
  """
  Checks if the graph has an independent vertex cover of size at least k.

  Args:
      graph: Adjacency list representation of the graph.
      k: Minimum size of the independent vertex cover.

  Returns:
      True if the graph has an independent vertex cover of size at least k, False otherwise.
  """
  def dfs(node, visited, current_cover):
    """
    Depth-First Search to find an independent vertex cover.

    Args:
        node: Current node being explored.
        visited: Set of visited nodes.
        current_cover: Current set of vertices in the cover.

    Returns:
        True if an independent vertex cover of size at least k is found, False otherwise.
    """
    if len(current_cover) >= k:  # Found a cover of size at least k, return True
      return True
    visited.add(node)
    
    for neighbor in graph[node]:
      if neighbor not in visited:
        # Explore two options: include or exclude neighbor in the cover
        if dfs(neighbor, visited.copy(), current_cover):
          return True  # Found a cover through the neighbor branch
        current_cover.add(neighbor)  # Explore excluding the neighbor

    return False  # No cover found in this DFS branch

  # Start DFS from an arbitrary node
  for node in graph:
    if dfs(node, set(), set()):
      return True
  return False  # No cover found starting from any node

# Example usage
graph = {
    0: [1, 3],
    1: [0, 2],
    2: [1, 4],
    3: [0],
    4: [2]
}
k = 2

if has_independent_vertex_cover_of_size_k(graph, k):
  print("Graph has an independent vertex cover of size at least", k)
else:
  print("Graph does not have an independent vertex cover of size at least", k)


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


################################################################  
  
if has_independent_vertex_cover_of_size_k(graph, k):
  print("Graph has an independent vertex cover of size at least", k)
else:
  print("Graph does not have an independent vertex cover of size at least", k)
