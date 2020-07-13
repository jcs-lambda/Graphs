"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
        else:
            raise KeyError(f'duplicate vertex: {vertex_id}')

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 not in self.vertices:
            raise KeyError(f'unknown vertex: {v1}')
        elif v2 not in self.vertices:
            raise KeyError(f'unknown vertex: {v2}')
    
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id not in self.vertices:
            raise KeyError(f'unknown vertex: {vertex_id}')
        
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        visited = set()
        queue = Queue()
        queue.enqueue(starting_vertex)

        while queue.size() > 0:
            vertex = queue.dequeue()
            if vertex not in visited:
                visited.add(vertex)
                print(vertex)
                for edge in self.get_neighbors(vertex):
                    queue.enqueue(edge)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        visited = set()
        stack = Stack()
        stack.push(starting_vertex)

        while stack.size() > 0:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                print(vertex)
                for edge in self.get_neighbors(vertex):
                    stack.push(edge)

    def dft_recursive(self, starting_vertex, visited = set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex not in visited:
            visited.add(starting_vertex)
            print(starting_vertex)
            for edge in self.get_neighbors(starting_vertex):
                self.dft_recursive(edge, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        paths = []
        visited = set()
        queue = Queue()
        queue.enqueue([starting_vertex])

        while queue.size() > 0:
            path = queue.dequeue()
            vertex = path[-1]
            if vertex == destination_vertex:
                paths.append(path)
                continue
            if vertex not in visited:
                visited.add(vertex)
                for edge in self.get_neighbors(vertex):
                    new_path = path + [edge]
                    queue.enqueue(new_path)
        
        return self._min_path(paths)  

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        paths = []
        visited = set()
        stack = Stack()
        stack.push([starting_vertex])

        while stack.size() > 0:
            path = stack.pop()
            vertex = path[-1]
            if vertex == destination_vertex:
                paths.append(path)
                continue
            if vertex not in visited:
                visited.add(vertex)
                for edge in self.get_neighbors(vertex):
                    new_path = path + [edge]
                    stack.push(new_path)
        
        return self._min_path(paths)

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        paths = []
        visited = set()

        def recurse(path):
            vertex = path[-1]
            if vertex == destination_vertex:
                paths.append(path)
            elif vertex not in visited:
                visited.add(vertex)
                for edge in self.get_neighbors(vertex):
                    new_path = path + [edge]
                    recurse(new_path)

        recurse([starting_vertex])

        return self._min_path(paths)

    def _min_path(self, paths):
        """
        Returns the first, shortest list from a list of lists or None
        if list of lists is empty.
        """        
        min_path = min_steps = None

        for path in paths:
            steps = len(path)
            if min_steps is None or steps < min_steps:
                min_path = path
                min_steps = steps
        
        return min_path

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
