class StateAndReward:
    """State discretization and reward helpers for the Q-learning controller."""

    @staticmethod
    def get_state_angle(angle, vx, vy):
        """State discretization function for the angle controller."""

        # Exercise 1a: Discretize the angle and return a unique state.
        #============== Implementation ====================
        if angle < -0.4:
            state = "hard_left"
        elif angle < -0.1:
            state = "slight_left"
        elif angle <= 0.1:
            state = "upright"
        elif angle <= 0.4:
            state = "slight_right"
        else:
            state = "hard_right"

        #print(state)
        #==================================================
        return state

    @staticmethod
    def get_reward_angle(angle, vx, vy):
        """Reward function for the angle controller."""

        # Exercise 1b: Return a reward that favors an upright rocket.
        #============== Implementation ====================
        reward = max(0.0, 10.0 - 30.0 * abs(angle)) # Max point is 10 | 10/30 ≈ 0.33, so if angle is bigger than 0.33 rad points recived is 0
        #print(reward)
        #==================================================
        return reward

    @staticmethod
    def get_state_hover(angle, vx, vy):
        """State discretization function for the full hover controller."""

        # Exercise 4a: Build a state from angle, vx, and vy.
        #============== Implementation ====================
        angle_bin = StateAndReward.discretize(angle, 5, -0.4, 0.4)

        vx_bin = StateAndReward.discretize(vx, 3, -15, 15.0)

        vy_bin = StateAndReward.discretize(vy, 5, -10.0, 10.0)

        return f"a{angle_bin}_x{vx_bin}_y{vy_bin}"
        #==================================================
    @staticmethod
    def get_reward_hover(angle, vx, vy):
        """Reward function for the full hover controller."""

        # Exercise 4b: Return a reward for hovering.
        #============== Implementation ====================
        r_angle = max(0.0, 10.0 - 30.0 * abs(angle))
        r_vx = max(0.0, 8.0 - 2.0 * abs(vx))
        r_vy = max(0.0, 8.0 - 0.7 * abs(vy))

        return r_angle + r_vx + r_vy
        #==================================================
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
