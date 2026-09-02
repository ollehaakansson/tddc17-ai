from typing import List
import heapq
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch


class AStarNode(SearchNode):    
    # A* node with heuristic cost
    def __init__(self, state, parent=None, cost=0.0, heuristic=0.0):
        super().__init__(state, parent, None, cost)
        self.heuristic = heuristic
    
    # Compare nodes by f(n) = g(n) + h(n)
    # g(n) = cost[n], h(n) = heuristic[n]
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class AStarSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        self.path = []
        self.frontier = []
        self.explored = []

        initial_state = problem.get_initial_state()

        # Calc heuristic for init state
        heuristic = initial_state.distance_manhattan(problem.goal_state)

        initial_node = AStarNode(initial_state, None, 0.0, heuristic)
        # A* priority que
        heapq.heappush(self.frontier, initial_node)

        best_cost = {initial_state: 0.0}
        
        while self.frontier:
            # get node with lowest f(n)
            current_node = heapq.heappop(self.frontier)
            current_state = current_node.get_state()

            # skip outdated nodes with a worse cost
            if current_node.get_cost() > best_cost[current_state]:
                continue

            #Check if we already reached the goal
            if problem.is_goal_state(current_state):
                self.path = current_node.get_path_from_root()
                return self.path

            self.explored.append(current_node)

            # Get all possible successors
            successors = problem.get_successors(current_state)

            for successor in successors:
                new_cost = current_node.get_cost() + 1
                
                # Add successor if it is new or is reached with a cheaper path
                if successor not in best_cost or new_cost < best_cost[successor]:
                    best_cost[successor] = new_cost
                    
                    # Manhattan distance is used as heuristic
                    heuristic = successor.distance_manhattan(problem.goal_state)
                    node = AStarNode(successor, current_node, new_cost, heuristic)

                    heapq.heappush(self.frontier, node)

        return []
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)

    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)
    