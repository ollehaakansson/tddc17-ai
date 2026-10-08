## 1. Describe your state representation, reward function, and actions.

### State Representation
The continuous rocket angle is discretized into 5 discrete states to keep the state space small and allow rapid training:
hard_left: angle < -0.4 rad
slight_left: -0.4 <= angle < -0.1 rad
upright: -0.1 <= angle <= 0.1 rad
slight_right: 0.1 < angle <= 0.4 rad
hard_right: angle > 0.4 rad

### Reward Function
We use a continuous linear reward function that favors an upright rocket:

reward = max(0.0, 10.0 - 30.0 * abs(angle))

The agent receives a maximum reward of 10.0 when the rocket is perfectly upright (angle = 0). If the tilt exceeds approximately 0.33 rad (10 / 30 ≈ 0.33), the reward decreases to 0.0 to heavily discourage large deviations

### Actions
The controller uses 4 discrete actions based on the 3 available engines:
Action 0: No engines firing
Action 1: Middle engine firing
Action 2: Left engine firing (applies torque to rotate right)
Action 3: Right engine firing (applies torque to rotate left)

## 2. Explain each part of the Q-learning update in your own words. What does a Q-value represent?
A Q-value, Q(s, a), is a score that tells the rocket how good a choice is in the long run. It does not just look at what happens right now, but estimates how much total reward the rocket can collect in the future if it picks action a while being in state s.

The formula used to update the table is:

Q(s, a) <- Q(s, a) + alpha * (r + gamma * max Q(s', a') - Q(s, a))

Here is what each part means:
**Q(s, a) (Old guess):** 
The score we already had saved in our table for this action in this state.

**r (Immediate reward):** 
The points the rocket gets right away for taking this action (for example, points for staying upright).

**max Q(s', a') (Best next step):**
The highest score the rocket can get from the new position it landed in.

**gamma:**
A number close to 1 that makes future rewards worth slightly less than points earned right now.

**(r + gamma * max Q(s', a') - Q(s, a)):** 
The difference between what actually happened (points right now + best future points) and what the rocket originally guessed. If this is positive, things went better than expected.

**alpha:** 
How much the rocket changes its old guess based on the new result. In the beginning it learns fast, but after trying the same move many times, alpha gets smaller so the values stay stable and stop jumping around.

## 3. Switch exploration off before learning starts. What happens, and why?
The rocket fails to balance and repeatedly crashes without ever learning how to fly.

Why This Happens:
At the start, every state-action pair starts at 0.0 in the Q-table. And with exploration switched off, the controller strictly follows a greedy policy, always choosing the action with the highest Q-value (which will be 0). Then, because it never explores random actions, the rocket never tries firing other engines when tilting and remains stuck repeating the same non-optimal choice.

## In your report, describe your hover state and reward functions. Explain the choices you made and how the size of the state space affected learning.
### State Function
To get the rocket hover, we look at three things: angle, vertical speed, and horizontal speed:

**Angle (5 bins):**
We split the angle into 5 boxes so the rocket knows if it is standing straight, tilting a little, or about to tip over completely.

**Horizontal Speed (3 bins):**
We only need 3 boxes here to see if the rocket is drifting left, standing still, or drifting right. This keeps things simple and saves memory.

**Vertical Speed (5 bins):**
Because gravity pulls down and the main engine pushes up, the rocket speeds up and down very fast. We use 5 boxes so it knows if it is falling fast, falling slowly, staying still in the air, going up slowly, or shooting up too fast.

By putting these together, we get 5 * 5 * 3 = 75 different situations (states). Since the rocket can choose between 4 actions, the table needs to learn 75 * 4 = 300 different combinations in total.


### Reward Function
The total reward combines feedback from the angle, horizontal speed, and vertical speed by adding them together:

total_reward = r_angle + r_vx + r_vy

**Angle (0 to 10 points, zero reward at ang >= 0.33 rad):**
Staying upright is the highest priority because if the rocket flips over, it cannot fly or recover at all.

**Horizontal speed (0 to 8 points, zero reward at |vx| >= 4.0):**  
The side engines are primarily meant to balance the rocket, so we want sideways drifting to stop quickly. A speed over 4.0 already carries the rocket toward the screen boundaries, so we stop giving points when it drifts that fast.

**Vertical speed (0 to 8 points, zero reward at |vy| >= 11.4):**  
The vertical movement has both gravity (pulling down) and a very strong main rocket engine (pushing up) working on it. Because these forces are large, vertical speed changes naturally swing higher without immediately causing a crash. A wider tolerance of 11.4 gives the rocket enough room to brake and stabilize without losing all its points instantly.