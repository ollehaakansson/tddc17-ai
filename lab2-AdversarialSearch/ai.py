import random

from game import AI, State, Objective


class Random(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()

        available_moves = state.available_moves()
        if not available_moves:
            return None

        return random.choice(available_moves)


class MinMax(AI):
    MAX_DEPTH = None # Changed from 8.

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        moves = current_state.available_moves()
        if not moves:
            return None

        counter = [1]  # The root is expanded when we inspect its legal moves.
        # Positive scores favor player 0 (MAX); negative scores favor player 1 (MIN).
        maximizing = objective == Objective.MAX
        best_value = float('-inf') if maximizing else float('inf')
        best_move = moves[0]

        for move in moves:
            # Try this pit, then assume both players choose their best replies.
            value = MinMax._value(current_state.next_state(move), 1, counter)
            # Strict comparison keeps the first legal move when scores are tied.
            if (maximizing and value > best_value) or (not maximizing and value < best_value):
                best_value, best_move = value, move

        print(f"[MinMax] Expanded states: {counter[0]}")
        return best_move

    @staticmethod
    def _value(state: State, depth: int, counter: list[int]):
        # Count depth in moves, including consecutive turns by the same player.
        # At a finished game or the depth limit, use the states score as a leaf value.
        if state.check_victory() is not None or (MinMax.MAX_DEPTH is not None and depth >= MinMax.MAX_DEPTH):
            return state.score

        moves = state.available_moves()
        # Only states whose children we explore count as expanded states.
        counter[0] += 1
        # The next player comes from the state, a move into a store grants another turn.
        values = (MinMax._value(state.next_state(move), depth + 1, counter) for move in moves)
        return max(values) if state.current_player == 0 else min(values)


class AlphaBeta(AI):
    MAX_DEPTH = None # Changed from 8.

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        # Search every root move, pruning happens in the recursive branches.
        moves = current_state.available_moves()
        if not moves:
            return None

        counter = [1]
        pruned = [0]  # Number of child branches skipped
        maximizing = objective == Objective.MAX
        # Alpha is MAXs best guaranteed score, beta is MINs best guaranteed score.
        alpha, beta = float('-inf'), float('inf')
        best_value = alpha if maximizing else beta
        best_move = moves[0]

        for move in moves:
            value = AlphaBeta._value(current_state.next_state(move), 1, alpha, beta, counter, pruned)
            if (maximizing and value > best_value) or (not maximizing and value < best_value):
                best_value, best_move = value, move
            # Pass the best root bound found so far into the next branch.
            if maximizing:
                alpha = max(alpha, best_value)
            else:
                beta = min(beta, best_value)

        print(f"[AlphaBeta] Expanded states: {counter[0]}; pruned branches: {pruned[0]}")
        return best_move

    @staticmethod
    def _value(state: State, depth: int, alpha: float, beta: float,
               counter: list[int], pruned: list[int]):
        # Use exactly the same leaf evaluation as MinMax.
        if state.check_victory() is not None or (AlphaBeta.MAX_DEPTH is not None and depth >= AlphaBeta.MAX_DEPTH):
            return state.score

        moves = state.available_moves()
        counter[0] += 1
        # An extra turn leaves current_player unchanged, so do not alternate by depth.
        maximizing = state.current_player == 0
        best_value = float('-inf') if maximizing else float('inf')

        for index, move in enumerate(moves):
            value = AlphaBeta._value(state.next_state(move), depth + 1, alpha, beta, counter, pruned)
            if maximizing:
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
            else:
                best_value = min(best_value, value)
                beta = min(beta, best_value)

            # Alpha >= beta means an ancestor already has a better choice.
            # Count the unvisited sibling branches, then stop searching here.
            if alpha >= beta:
                pruned[0] += len(moves) - index - 1
                break

        return best_value
