
## 3.1 First implementation

### 1. Suppose that we allow 5 seconds for the AI player to choose its next move.

#### a) What are the maximum dimensions of the board (number of pits and seeds) that allow this?

Among the tested boards where n = m, the largest that stayed below 5 seconds was n = m = 3. The first three moves took approximately 2.73, 1.45 and 0.58 seconds. With n = m = 4, the first move did not finish within 45 seconds.

There is no single maximum pair if pits and seeds are varied independently, since we can trade more seeds for fewer pits. These results are therefore for equal dimensions, and the times depend on the machine and the current board state.

#### b) How many nodes are then expanded?

For n = m = 3, the first move expanded 725,083 nodes. The following two moves expanded 232,394 and 100,175 nodes.

### 2. For a small game, let the algorithm you implemented play against itself.

#### a) Which player won?

With n = m = 3 and no depth cutoff, player 0 won with 11 seeds in its store against player 1's 7 seeds.

#### b) What does it mean? Do you think that, as player 1, you could beat MinMax as player 0?

Both players search all the way to the end and assume that the opponent makes the best possible moves. Player 0 winning therefore means that this starting position has a winning strategy for player 0.

As player 1, we could not beat a correctly implemented, unbounded MinMax playing as player 0 on this board. MinMax already considers our best possible replies. This conclusion applies to this starting position; other board dimensions can have different outcomes.

In Kalah, a move can also give an extra turn. Therefore, MAX and MIN must be chosen from the state's current player, rather than simply alternating at every depth.

## 3.2 Depth-bounded MinMax

### 1. What score function did you choose? Justify the intuition behind it.

For a non-terminal state, our score function is:

score = 2 · (store_0 - store_1) + (side_0 - side_1)

Here, side_0 and side_1 are the sums of the seeds in each player's ordinary pits.

Seeds in a store are already secured, so we give them twice the weight of seeds still on the board. Seeds on our own side can still become points, but they might also be captured or distributed to the other side. A positive score favors player 0, while a negative score favors player 1.

For a terminal state, let N be the total number of seeds:
Player 0 wins: score = 3 · N + (store_0 - store_1).
Player 1 wins: score = -3 · N + (store_0 - store_1).
Tie: score = 0.

The large win/loss bonus makes a finished win more valuable than any non-terminal heuristic score. The store difference also makes the algorithm prefer a larger winning margin when the outcome is otherwise the same.

### 2. Just like before, suppose that we allow 5 seconds for the AI player to choose its next move.

#### a) What are the maximum dimensions of the board (number of pits and seeds) that allow this?

With the depth cutoff set to 8, the largest tested board with equal dimensions that stayed below 5 seconds per move was n = m = 6. The first three moves took approximately 2.86, 4.16 and 4.77 seconds.

For comparison, n = m = 7 took approximately 14.55 seconds for the first move in another run. As before, this is a comparison of equal dimensions rather than a maximum over every possible combination of pits and seeds.

#### b) How many nodes are then expanded?

For n = m = 6 and a cutoff of 8, the first move expanded 217,382 nodes. The next two moves expanded 189,095 and 216,713 nodes.

The depth counts individual moves, including extra turns by the same player.

### 3. Find some dimensions of the board such that, on your machine, the original (non-depth-bounded) algorithm takes 30 to 40 seconds to compute the first few moves.

We used n = 2 pits per player and m = 28 seeds per pit. Full MinMax took approximately 32.59 seconds in total for the first three moves.

#### a) At which (minimum) value should the cutoff be set so that depth-bounded MinMax achieves comparable results to MinMax?

If comparable results means choosing the same first three moves, the minimum cutoff in this test was 5.

Full MinMax chose pits 1, 4 and 0, using the pit identifiers from the code. Cutoffs 1 through 4 chose pit 0 for the first move, while cutoff 5 chose the same three moves as full MinMax.

This does not prove that cutoff 5 plays optimally throughout the whole game. The required depth depends on the position and the score function, and matching a few moves is only a limited comparison.

#### b) How many nodes do the algorithms then expand, respectively? How much faster is the depth-bounded algorithm?

| Move | Full MinMax: expanded nodes | Full MinMax: time | Cutoff 5: expanded nodes | Cutoff 5: time |
| --- | ---: | ---: | ---: | ---: |
| 1 | 4,614,774 | 18.62 s | 31 | 0.000234 s |
| 2 | 2,167,224 | 8.77 s | 29 | 0.000179 s |
| 3 | 1,177,827 | 5.20 s | 27 | 0.000165 s |
| Total | 7,959,825 | 32.59 s | 87 | 0.000578 s |

In this test, depth-bounded MinMax was approximately 56,000 times faster. The bounded searches take less than a millisecond, so their exact timing and the speedup are sensitive to measurement noise.

### 4. Suppose that we set the cutoff to depth 1. How is that search then called?

This is a greedy, one-ply search. It evaluates the states directly after each available move and chooses the one with the best immediate score, without considering any further moves or the opponent's reply.

## 4 Alpha-Beta Pruning

### 1. When the value for the depth cutoff is the same for both algorithms, how do the outputs of Alpha-Beta compare to the ones of MinMax? Justify.

With the same cutoff and score function, Alpha-Beta returns the same MinMax value and an equally good move. In our implementation, both algorithms examine moves in the same order and keep the first move when values are tied, so they also choose the same pit.

Alpha-Beta only skips branches that cannot change the decision. Alpha is a lower bound on what MAX can guarantee, and beta is an upper bound on what MIN can guarantee. When alpha >= beta, an ancestor already has an alternative that makes the rest of that branch irrelevant.

Therefore, pruning changes the amount of work, rather than the result. Its benefit depends on move ordering: finding strong moves early usually allows more pruning.

### 2. Find some dimensions of the board such that, on your machine, depth-bounded MinMax takes 30 to 40 seconds to compute the first few moves.

We used n = 7 pits per player and m = 8 seeds per pit, with a depth cutoff of 8. Depth-bounded MinMax took approximately 35.68 seconds in total for the first two moves.

#### a) How long does Alpha-Beta take to perform the same moves?

Alpha-Beta took approximately 0.187 seconds in total for the same two moves, making it about 191 times faster. Both algorithms chose pits 3 and 12.

#### b) How many nodes are expanded?

| Move | MinMax: expanded nodes | MinMax: time | Alpha-Beta: expanded nodes | Alpha-Beta: time | Pruned branches |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 751,432 | 17.90 s | 12,807 | 0.0923 s | 48,609 |
| 2 | 695,465 | 17.79 s | 12,707 | 0.0949 s | 46,640 |
| Total | 1,446,897 | 35.68 s | 25,514 | 0.1872 s | 95,249 |

The pruned-branches counter counts skipped immediate child branches, rather than every node that would have existed below them. Both algorithms use the same definition of an expanded node.

## Bonus questions

### How could the difficulty/strength of the AI be tuned?

The simplest option is to change the depth cutoff. A smaller cutoff makes the AI faster and usually weaker, while a larger cutoff lets it consider more consequences of each move. Improving the score function can also make the AI stronger.

For an easier opponent, we could sometimes select a random legal move instead of the best move. Alpha-Beta does not make the AI stronger at the same depth, but its time savings can allow a deeper search within the same time budget.

### Is it a good idea to simply limit the search time, and cut the search of the unbounded algorithm when it runs out of time?

Simply stopping an unbounded depth-first search is not a good idea. It may spend all its time on the first root branch before comparing the other available moves. The result would then depend heavily on move ordering, and we might not even have a fully evaluated move to return.

A better approach is iterative deepening: complete a search at depth 1, then depth 2, and so on. We keep the best move from the last completed depth and return it when the time runs out. A legal fallback move can be kept in case even the first iteration cannot finish. This can be combined with Alpha-Beta pruning.
