1. What is the difference between Breadth-First Search and Uniform Cost Search in a domain where the cost of each action is 1

    BFS expands nodes based on their depth, while UCS expands nodes based on their accumulated path cost. 
    So if every action has a cost of 1, the path cost is equal to the depth of the node.
    Therefore, BFS and UCS behave pretty much the same and will both always find the shortest paths.

2. Suppose that h_1 and h_2 are admissible heuristics (used in A*). Which of the following are also admissible? Justify your answers.

(Admissible = the heuristic doesn't overestimate the true cost.)

    a) ADMISSIBLE: Since both h_1 and h_2 never overestimate the true remainin cost, their average wouldn't either.
    b) MAYBE but risky: Even if h_1 doesnät overestimate the true cost, multiplying it by 2 might. And if it does then it isn't admissable.
    c) ADMISSIBLE: Since both h_1 and h_2 already are admissible, then neither can be larger than the true remaining cost.

3. For each of the following search algorithms, determine whether they are complete and optimal. Give a quick explanation why.

    - BFS
        - 
    - DFS
        - 
    - UCS
        - 
    - Iterative Deepening Search
        - 
    - Bidirectionnal Search
        - 
    - Greedy Best-First Search
        - 
    - A* Search
        - 