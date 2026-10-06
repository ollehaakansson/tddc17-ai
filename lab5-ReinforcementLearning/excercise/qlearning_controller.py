import random
import time

from state_and_reward import StateAndReward


class QLearningController:
    """Student controller for the tabular Q-learning exercises."""

    # Exercise 2: Keep this equal to the number of actions implemented in
    # perform_action.
    NUM_ACTIONS = 4

    # Parameters of the learning algorithm. These may be tuned.
    GAMMA_DISCOUNT_FACTOR = 0.95
    LEARNING_RATE_CONSTANT = 10
    REPEAT_ACTION_MAX = 30

    def __init__(self):
        # The simulator sets this before calling init().
        self.object = None

        # Agent senses.
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None
        self.angle = None

        # Agent actuators.
        self.left_engine = None
        self.middle_engine = None
        self.right_engine = None

        # Keep track of the previous state and action.
        self.previous_state = None
        self.previous_vx = 0
        self.previous_vy = 0
        self.previous_angle = 0
        self.previous_action = 0

        # Tables used by Q-learning.
        self.qtable = {}
        self.ntable = {}

        self.explore_chance = 0.5

        # Internal counters.
        self.iteration = 0
        self.action_counter = 0
        self.print_counter = 0

        # Internal helper variables.
        self.paused = False
        self.explore = True
        self.cso = None
        self.last_pressed_explore = 0

    def init(self):
        # Tutorial: This is where the controller obtains its sensors and
        # engines from the simulated rocket.
        self.cso = self.object
        self.x = self.cso.getObjectById("x")
        self.y = self.cso.getObjectById("y")
        self.vx = self.cso.getObjectById("vx")
        self.vy = self.cso.getObjectById("vy")
        self.angle = self.cso.getObjectById("angle")

        self.previous_vy = self.vy.getValue()
        self.previous_vx = self.vx.getValue()
        self.previous_angle = self.angle.getValue()

        self.left_engine = self.cso.getObjectById("rocket_engine_left")
        self.right_engine = self.cso.getObjectById("rocket_engine_right")
        self.middle_engine = self.cso.getObjectById("rocket_engine_middle")

    def reset_rockets(self):
        """Turn off all rockets."""
        self.left_engine.setBursting(False)
        self.right_engine.setBursting(False)
        self.middle_engine.setBursting(False)

    def perform_action(self, action):
        """Perform the chosen action."""

        # Exercise 2: Map every action number to an engine activation pattern.
        # Explicitly switch off every engine that the action does not use.
        self.reset_rockets()

    def tick(self, current_time):
        """Main decision loop. Called every iteration by the simulator."""
        self.iteration += 1

        if self.paused:
            return

        # Exercise 4: Change these angle functions to the hover functions after
        # the angle controller works.
        new_state = StateAndReward.get_state_angle(
            self.angle.getValue(),
            self.vx.getValue(),
            self.vy.getValue(),
        )

        # Repeat the chosen action for a while, hoping to reach a new state.
        # This is a trick to speed up learning on this problem.
        self.action_counter += 1
        if (
            new_state == self.previous_state
            and self.action_counter < self.REPEAT_ACTION_MAX
        ):
            return

        previous_reward = StateAndReward.get_reward_angle(
            self.previous_angle,
            self.previous_vx,
            self.previous_vy,
        )
        self.action_counter = 0

        # The agent is in a new state, do learning and action selection.
        if self.previous_state is not None:
            # Create state-action key.
            prev_stateaction = f"{self.previous_state}{self.previous_action}"

            # Increment state-action counter.
            if prev_stateaction not in self.ntable:
                self.ntable[prev_stateaction] = 0
            self.ntable[prev_stateaction] += 1

            # Update Q value.
            if prev_stateaction not in self.qtable:
                self.qtable[prev_stateaction] = 0.0

            # Exercise 3: Implement the Q-learning update here. Use
            # previous_reward, alpha(), GAMMA_DISCOUNT_FACTOR, and
            # get_max_action_q_value().

            action = self.select_action(new_state)
            self.perform_action(action)

            # Only print every 10th line to reduce spam.
            self.print_counter += 1
            if self.print_counter % 10 == 0:
                print(
                    "ITERATION: "
                    f"{self.iteration} "
                    "SENSORS: "
                    f"a={self.angle.getValue():.3f} "
                    f"vx={self.vx.getValue():.3f} "
                    f"vy={self.vy.getValue():.3f} "
                    f"P_STATE: {self.previous_state} "
                    f"P_ACTION: {self.previous_action} "
                    f"P_REWARD: {previous_reward:.3f} "
                    f"P_QVAL: {self.qtable[prev_stateaction]:.3f} "
                    f"Tested: {self.ntable[prev_stateaction]} times."
                )

            self.previous_vy = self.vy.getValue()
            self.previous_vx = self.vx.getValue()
            self.previous_angle = self.angle.getValue()
            self.previous_action = action

        self.previous_state = new_state

    def alpha(self, num_tested):
        """Compute learning rate alpha from the state-action test count."""
        return self.LEARNING_RATE_CONSTANT / (
            self.LEARNING_RATE_CONSTANT + num_tested
        )

    def get_max_action_q_value(self, state):
        """Find the highest Q-value of any action in the given state."""
        max_qval = float("-inf")

        for action in range(self.NUM_ACTIONS):
            qval = self.qtable.get(f"{state}{action}")
            if qval is not None and qval > max_qval:
                max_qval = qval

        if max_qval == float("-inf"):
            # Assign 0 as that corresponds to initializing the Qtable to 0.
            max_qval = 0

        return max_qval

    def select_action(self, state):
        """Select an action based on Q-values and the exploration chance."""
        action = 0

        # May do exploratory move if in exploration mode.
        if self.explore and abs(random.random()) < self.explore_chance:
            return random.randrange(self.NUM_ACTIONS)

        # Find action with highest Q-value in the given state.
        max_qval = float("-inf")
        for i in range(self.NUM_ACTIONS):
            test_pair = f"{state}{i}"
            qval = self.qtable.get(test_pair, 0)
            if qval > max_qval:
                max_qval = qval
                action = i

        return action

    def toggle_explore(self):
        """The E key toggles exploration mode."""
        # Make sure we do not toggle it multiple times.
        now = int(time.time() * 1000)
        if now - self.last_pressed_explore < 1000:
            return

        if self.explore:
            print("Turning OFF exploration!")
            self.explore = False
        else:
            print("Turning ON exploration!")
            self.explore = True

        self.last_pressed_explore = now

    def pause(self):
        self.paused = True
        self.reset_rockets()

    def run(self):
        self.paused = False
