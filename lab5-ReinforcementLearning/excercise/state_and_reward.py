class StateAndReward:
    """State discretization and reward helpers for the Q-learning controller."""

    @staticmethod
    def get_state_angle(angle, vx, vy):
        """State discretization function for the angle controller."""

        # Exercise 1a: Discretize the angle and return a unique state.

        state = "angle-state-not-implemented"

        return state

    @staticmethod
    def get_reward_angle(angle, vx, vy):
        """Reward function for the angle controller."""

        # Exercise 1b: Return a reward that favors an upright rocket.

        reward = 0

        return reward

    @staticmethod
    def get_state_hover(angle, vx, vy):
        """State discretization function for the full hover controller."""

        # Exercise 4a: Build a state from angle, vx, and vy.

        state = "hover-state-not-implemented"

        return state

    @staticmethod
    def get_reward_hover(angle, vx, vy):
        """Reward function for the full hover controller."""

        # Exercise 4b: Return a reward for hovering.

        reward = 0

        return reward

    @staticmethod
    def discretize(value, nr_values, min_value, max_value):
        """Uniform discretization with explicit underflow and overflow bins.

        Returns an integer between 0 and nr_values - 1.

        If value is lower than min_value, 0 is returned. If value is higher
        than max_value, nr_values - 1 is returned. Otherwise a value between
        1 and nr_values - 2 is returned.
        """
        if nr_values < 2:
            return 0

        diff = max_value - min_value

        if value < min_value:
            return 0
        if value > max_value:
            return nr_values - 1

        temp_value = value - min_value
        ratio = temp_value / diff

        return int(ratio * (nr_values - 2)) + 1

    @staticmethod
    def discretize2(value, nr_values, min_value, max_value):
        """Uniform discretization without separate inner edge bins.

        Returns an integer between 0 and nr_values - 1.
        """
        diff = max_value - min_value

        if value < min_value:
            return 0
        if value > max_value:
            return nr_values - 1

        temp_value = value - min_value
        ratio = temp_value / diff

        return int(ratio * nr_values)
