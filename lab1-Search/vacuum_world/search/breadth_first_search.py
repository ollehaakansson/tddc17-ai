from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch

from collections import deque

class BreadthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        self.path = []
            
        initial_state = problem.get_initial_state()
        initial_node = SearchNode(initial_state, None, None, 0.0)

        # BFS queue
        queue = deque([initial_node])

        # A visited list to keep the algorithm gooing in circles checking the same node over and over agian
        visited = {initial_state}

        steps = 0
            
        while queue and steps < self.max_depth:
            current_node = queue.popleft()
            current_state = current_node.get_state()

            # Check if we've reached the goal
            if problem.is_goal_state(current_state):
                self.path = current_node.get_path_from_root()
                return self.path

            # Get all possible successors
            successors = problem.get_successors(current_state)

            for successor in successors:
                if successor not in visited:
                    node = SearchNode(successor, current_node, None, current_node.get_cost() + 1)
                    queue.append(node)
                    visited.add(successor)

            steps += 1
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return []
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return []