#!/usr/bin/env python3
"""Student file for optional Deep Q-learning from image observations."""

from __future__ import annotations

import random
from collections import deque

try:
    import torch
    import torch.nn as nn
except ImportError as error:
    raise SystemExit(
        "This optional part requires PyTorch. Run with: "
        "uv run python deep_q_learning.py"
    ) from error

from simulator import SimulatorApp


NUM_ACTIONS = 4


class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        # Exercise 5a (optional): Define a CNN that maps a 64x64 grayscale
        # image to NUM_ACTIONS Q-values. The output shape must be
        # [batch_size, NUM_ACTIONS].
        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 64, NUM_ACTIONS),
        )

    def forward(self, x):
        return self.network(x)


def frame_to_tensor(frame):
    return torch.tensor(frame, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.0


def perform_action(rocket, action):
    rocket.left_engine.setBursting(False)
    rocket.middle_engine.setBursting(False)
    rocket.right_engine.setBursting(False)

    # Same action set as the tabular Q-learning solution.
    if action == 1:
        rocket.middle_engine.setBursting(True)
    elif action == 2:
        rocket.left_engine.setBursting(True)
    elif action == 3:
        rocket.right_engine.setBursting(True)


def select_action(policy_net, state, epsilon):
    # Exercise 5b (optional): Implement epsilon-greedy action selection.
    del policy_net, state, epsilon
    return random.randrange(NUM_ACTIONS)


def optimize_model(policy_net, target_net, optimizer, replay_buffer, batch_size, gamma):
    # Exercise 5c (optional): Sample a mini-batch and minimize the Deep
    # Q-learning loss:
    # L(theta) = mean((r + gamma * max_a' Q_target(s', a') - Q_theta(s, a))^2)
    return None


class DeepQController:
    """Live controller for the optional image-based exercise."""

    def __init__(self):
        self.object = None
        self.paused = False
        self.explore = True
        self.iteration = 0
        self.previous_action = 0
        self.last_reward = 0.0
        self.last_q_value = 0.0
        self.last_loss = 0.0
        self.episode = 1
        self.episode_steps = 0

        self.epsilon = 0.5
        self.gamma = 0.95
        self.batch_size = 32
        self.target_update = 500
        self.policy_net = DQN()
        self.target_net = DQN()
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=1e-3)
        self.replay_buffer = deque(maxlen=10_000)
        self.current_state = None

    def init(self):
        self.current_state = frame_to_tensor(self.object.get_cnn_frame())

    def tick(self, current_time):
        del current_time
        if self.paused:
            perform_action(self.object, 0)
            return

        self.iteration += 1
        self.previous_action = select_action(
            self.policy_net,
            self.current_state,
            self.epsilon if self.explore else 0.0,
        )
        perform_action(self.object, self.previous_action)

    def observe_step(self, terminal):
        # Survival is the only reward used in the image-based exercise.
        reward = 0.0 if terminal else 1.0
        next_state = frame_to_tensor(self.object.get_cnn_frame())
        self.replay_buffer.append(
            (self.current_state, self.previous_action, reward, next_state, terminal)
        )
        self.last_reward = reward
        self.episode_steps += 1

        loss = optimize_model(
            self.policy_net,
            self.target_net,
            self.optimizer,
            self.replay_buffer,
            self.batch_size,
            self.gamma,
        )
        if loss is not None:
            self.last_loss = float(loss)

        if self.iteration % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        self.current_state = next_state
        if terminal:
            print(
                f"episode={self.episode} survival={self.episode_steps} "
                f"replay={len(self.replay_buffer)} loss={self.last_loss:.4f}"
            )
            self.episode += 1
            self.reset_episode()

    def reset_episode(self):
        self.episode_steps = 0
        self.current_state = frame_to_tensor(self.object.get_cnn_frame())

    def pause(self):
        self.paused = True
        perform_action(self.object, 0)

    def run(self):
        self.paused = False

    def toggle_explore(self):
        self.explore = not self.explore
        state = "on" if self.explore else "off"
        print(f"Exploration is {state}.")


def main():
    app = SimulatorApp(controller_class=DeepQController, manual_mode=False)
    app.run()


if __name__ == "__main__":
    main()
