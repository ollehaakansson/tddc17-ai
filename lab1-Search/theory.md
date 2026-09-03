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
        - Is both complete and optimal in finite spaces where all vertices have the same cost. 
    - DFS
        - Is complete in finite spaces, but not optimal since it returns the first solution it finds. If it is a infinite space then dfs isn't complete
    - UCS
        - In this finite space and where all cost is the same then it is basically identical to bfs. So it is complete and optimal. Also works (optimal) even if the costs between states differ (which bfs doesn't)
    - Iterative Deepening Search
        - Is both complete and optimal in finite spaces where all vertices have the same cost. (Is combo of BFS & DFS)
    - Bidirectionnal Search
        - It performs 2 searches at once, one from the goal and one from the inital. If you for example use BFS to explore from both directions then it will be complete (for finite spaces) and optimal (in spaces where all vertices cost the same)
    - Greedy Best-First Search
        - It is complete in finite spaces (when repeated states are avoided). It is not optimal however since it only takes h(n) into account and ignores the path cost.
    - A* Search
        - It is complete and optimal. Works like a bfs but has a heuristic aspect where it priotitize directions pointing to the goals destination.
