#!/usr/bin/env python3
"""Pygame rocket simulator for the Q-learning controller exercise."""

from __future__ import annotations

import math
import time

import pygame

from qlearning_controller import QLearningController

WORLD_LEFT = -470
WORLD_RIGHT = 470
WORLD_TOP = -360
WORLD_BOTTOM = 330
LANDING_PAD_WIDTH = 300
LANDING_PAD_TOP = WORLD_BOTTOM - 22

WINDOW_SIZE = (1040, 760)
MIN_WINDOW_SIZE = (840, 620)
CONTROL_HEIGHT = 82


class DoubleFeature:
    def __init__(self, getter):
        self._getter = getter

    def getValue(self):
        return self._getter()


class RocketEngine:
    def __init__(self, name):
        self.name = name
        self._bursting = False

    def setBursting(self, bursting):
        self._bursting = bool(bursting)

    def isBursting(self):
        return self._bursting


class SimulatedRocket:
    """Simulator object exposed to the student controller."""

    def __init__(self):
        self.left_engine = RocketEngine("left")
        self.middle_engine = RocketEngine("middle")
        self.right_engine = RocketEngine("right")
        self.reset()

        self._objects = {
            "x": DoubleFeature(lambda: self.x),
            "y": DoubleFeature(lambda: self.y),
            "vx": DoubleFeature(lambda: self.vx),
            "vy": DoubleFeature(lambda: self.vy),
            "angle": DoubleFeature(lambda: self.angle),
            "rocket_engine_left": self.left_engine,
            "rocket_engine_middle": self.middle_engine,
            "rocket_engine_right": self.right_engine,
        }

    def getObjectById(self, object_id):
        return self._objects[object_id]

    def reset(self):
        self.x = 0.0
        self.y = 120.0
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.34
        self.angular_velocity = -0.16
        self.left_engine.setBursting(False)
        self.middle_engine.setBursting(False)
        self.right_engine.setBursting(False)

    def step(self, dt):
        gravity = 132.0
        linear_damping = 0.993
        angular_damping = 0.996
        main_thrust = 245.0
        side_thrust = 215.0
        torque_strength = 7.2

        ax = 0.0
        ay = gravity
        torque = 0.0

        if self.middle_engine.isBursting():
            tx, ty = self._body_thrust(main_thrust)
            ax += tx
            ay += ty

        if self.left_engine.isBursting():
            tx, ty = self._body_thrust(side_thrust)
            ax += tx
            ay += ty
            torque += torque_strength

        if self.right_engine.isBursting():
            tx, ty = self._body_thrust(side_thrust)
            ax += tx
            ay += ty
            torque -= torque_strength

        self.vx = (self.vx + ax * dt) * linear_damping
        self.vy = (self.vy + ay * dt) * linear_damping
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.angular_velocity = (
            self.angular_velocity + torque * dt
        ) * angular_damping
        self.angle += self.angular_velocity * dt
        self.angle = math.atan2(math.sin(self.angle), math.cos(self.angle))

        if self.y > WORLD_BOTTOM or abs(self.x) > WORLD_RIGHT or self.y < WORLD_TOP:
            self.reset()
            return True
        return False

    def _body_thrust(self, thrust):
        # Angle zero means upright. Positive y points downwards.
        return thrust * math.sin(self.angle), -thrust * math.cos(self.angle)

    def get_cnn_frame(self, flat=False):
        """Return a 64 by 64 grayscale observation of this rocket state."""
        renderer = ObservationRenderer(size=64)
        if flat:
            return renderer.render_flat(self)
        return renderer.render(self)


class ObservationRenderer:
    """CPU-only 64 by 64 grayscale observation renderer for CNN inputs."""

    def __init__(self, size=64):
        self.size = size

    def render(self, rocket):
        frame = [[24 for _ in range(self.size)] for _ in range(self.size)]

        self._draw_background(frame)
        self._fill_rect_world(
            frame,
            -LANDING_PAD_WIDTH / 2,
            LANDING_PAD_TOP,
            LANDING_PAD_WIDTH / 2,
            WORLD_BOTTOM,
            112,
        )
        self._fill_rect_world(frame, -58, LANDING_PAD_TOP - 8, 58, LANDING_PAD_TOP, 180)

        px, py = self._world_to_pixel(rocket.x, rocket.y)
        self._draw_rocket(frame, rocket, px, py)
        return frame

    def render_flat(self, rocket):
        return [value for row in self.render(rocket) for value in row]

    def _draw_background(self, frame):
        for y in range(self.size):
            value = int(22 + 38 * (y / (self.size - 1)))
            for x in range(self.size):
                frame[y][x] = value

        horizon = int(self.size * 0.72)
        for y in range(horizon, self.size):
            value = int(58 + 26 * ((y - horizon) / max(self.size - horizon - 1, 1)))
            for x in range(self.size):
                frame[y][x] = value

    def _draw_rocket(self, frame, rocket, px, py):
        angle = rocket.angle
        body = self._rotate_pixels(
            [(-1.4, -3.0), (1.4, -3.0), (1.8, 2.3), (0.8, 3.4), (-0.8, 3.4), (-1.8, 2.3)],
            px,
            py,
            angle,
        )
        nose = self._rotate_pixels([(0, -4.6), (-1.4, -3.0), (1.4, -3.0)], px, py, angle)
        left_fin = self._rotate_pixels([(-1.5, 1.0), (-3.2, 3.6), (-1.0, 3.0)], px, py, angle)
        right_fin = self._rotate_pixels([(1.5, 1.0), (3.2, 3.6), (1.0, 3.0)], px, py, angle)

        self._fill_polygon(frame, body, 220)
        self._fill_polygon(frame, nose, 175)
        self._fill_polygon(frame, left_fin, 145)
        self._fill_polygon(frame, right_fin, 145)

        if rocket.middle_engine.isBursting():
            self._fill_polygon(
                frame,
                self._rotate_pixels([(-0.7, 3.7), (0.7, 3.7), (0, 6.3)], px, py, angle),
                245,
            )
        if rocket.left_engine.isBursting():
            self._fill_polygon(
                frame,
                self._rotate_pixels([(-2.1, 3.5), (-1.0, 3.5), (-1.55, 5.4)], px, py, angle),
                220,
            )
        if rocket.right_engine.isBursting():
            self._fill_polygon(
                frame,
                self._rotate_pixels([(1.0, 3.5), (2.1, 3.5), (1.55, 5.4)], px, py, angle),
                220,
            )

    def _fill_rect_world(self, frame, x1, y1, x2, y2, value):
        px1, py1 = self._world_to_pixel(x1, y1)
        px2, py2 = self._world_to_pixel(x2, y2)
        left, right = sorted((int(px1), int(px2)))
        top, bottom = sorted((int(py1), int(py2)))
        for y in range(max(top, 0), min(bottom + 1, self.size)):
            for x in range(max(left, 0), min(right + 1, self.size)):
                frame[y][x] = value

    def _world_to_pixel(self, x, y):
        px = (x - WORLD_LEFT) / (WORLD_RIGHT - WORLD_LEFT) * (self.size - 1)
        py = (y - WORLD_TOP) / (WORLD_BOTTOM - WORLD_TOP) * (self.size - 1)
        return px, py

    def _rotate_pixels(self, points, px, py, angle):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        return [
            (px + x * cos_a - y * sin_a, py + x * sin_a + y * cos_a)
            for x, y in points
        ]

    def _fill_polygon(self, frame, points, value):
        min_x = max(int(math.floor(min(x for x, _ in points))), 0)
        max_x = min(int(math.ceil(max(x for x, _ in points))), self.size - 1)
        min_y = max(int(math.floor(min(y for _, y in points))), 0)
        max_y = min(int(math.ceil(max(y for _, y in points))), self.size - 1)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if self._point_inside_polygon(x + 0.5, y + 0.5, points):
                    frame[y][x] = value

    @staticmethod
    def _point_inside_polygon(x, y, points):
        inside = False
        prev_x, prev_y = points[-1]
        for curr_x, curr_y in points:
            if (curr_y > y) != (prev_y > y):
                x_intersect = (prev_x - curr_x) * (y - curr_y) / (prev_y - curr_y) + curr_x
                if x < x_intersect:
                    inside = not inside
            prev_x, prev_y = curr_x, curr_y
        return inside


class SimulatorApp:
    def __init__(self, controller_class=QLearningController, manual_mode=True):
        pygame.init()
        pygame.display.set_caption("Q-learning Rocket Simulator")
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 21)
        self.small_font = pygame.font.Font(None, 18)
        self.heading_font = pygame.font.Font(None, 25)

        self.rocket = SimulatedRocket()
        self.controller = controller_class()
        self.controller.object = self.rocket
        self.controller.init()

        self.manual_mode = manual_mode
        self.running = True
        self.pressed_keys = set()
        self.trail = []
        self.render_enabled = True
        self.sim_speed = 1
        self.speed_before_silent = self.sim_speed
        self.observation_renderer = ObservationRenderer(size=64)
        self.latest_cnn_frame = self.observation_renderer.render(self.rocket)
        self.buttons = []
        self.last_silent_draw = 0.0

    def run(self):
        while self.running:
            self._handle_events()
            self._simulate()
            self.latest_cnn_frame = self.observation_renderer.render(self.rocket)

            if self.render_enabled:
                self._draw()
                pygame.display.flip()
                self.clock.tick(60)
            else:
                now = time.perf_counter()
                if now - self.last_silent_draw >= 0.25:
                    self._draw_silent_status()
                    pygame.display.flip()
                    self.last_silent_draw = now

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                width = max(event.w, MIN_WINDOW_SIZE[0])
                height = max(event.h, MIN_WINDOW_SIZE[1])
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
                self._on_key_press(event.key)
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, command in self.buttons:
                    if rect.collidepoint(event.pos):
                        command()
                        break

    def _on_key_press(self, key):
        if key == pygame.K_SPACE:
            self.manual_mode = not self.manual_mode
            self._all_engines_off()
        elif key == pygame.K_p:
            self.controller.pause()
        elif key == pygame.K_o:
            self.controller.run()
        elif key == pygame.K_e:
            self.controller.toggle_explore()
        elif key == pygame.K_r:
            self._reset()
        elif key == pygame.K_g:
            self.toggle_rendering()
        elif key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
            self.speed_up()
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self.speed_down()

    def _simulate(self):
        for _ in range(self.sim_speed):
            if self.manual_mode:
                self._apply_manual_controls()
            else:
                self.controller.tick(int(time.perf_counter() * 1000))

            if not self.controller.paused:
                crashed = self.rocket.step(1 / 60)
                if hasattr(self.controller, "observe_step"):
                    self.controller.observe_step(crashed)
                if crashed and hasattr(self.controller, "register_terminal_reward"):
                    self.controller.register_terminal_reward(-80.0)

    def toggle_rendering(self):
        self.render_enabled = not self.render_enabled
        if self.render_enabled:
            self.sim_speed = self.speed_before_silent
        else:
            self.speed_before_silent = self.sim_speed
            self.sim_speed = 64

    def speed_up(self):
        self.sim_speed = min(self.sim_speed * 2, 64)

    def speed_down(self):
        self.sim_speed = max(self.sim_speed // 2, 1)

    def get_cnn_frame(self, flat=False):
        """Return the latest 64 by 64 grayscale frame for a CNN."""
        if flat:
            return [value for row in self.latest_cnn_frame for value in row]
        return [row[:] for row in self.latest_cnn_frame]

    def _apply_manual_controls(self):
        self.rocket.middle_engine.setBursting(pygame.K_UP in self.pressed_keys)
        self.rocket.left_engine.setBursting(pygame.K_LEFT in self.pressed_keys)
        self.rocket.right_engine.setBursting(pygame.K_RIGHT in self.pressed_keys)

        if pygame.K_DOWN in self.pressed_keys:
            self.rocket.vx *= 0.965
            self.rocket.vy *= 0.965
            self.rocket.angular_velocity *= 0.92

    def _all_engines_off(self):
        self.rocket.left_engine.setBursting(False)
        self.rocket.middle_engine.setBursting(False)
        self.rocket.right_engine.setBursting(False)

    def _reset(self):
        self.rocket.reset()
        for name, value in (
            ("previous_state", None),
            ("previous_vx", self.rocket.vx),
            ("previous_vy", self.rocket.vy),
            ("previous_angle", self.rocket.angle),
            ("previous_action", 0),
            ("action_counter", 0),
        ):
            if hasattr(self.controller, name):
                setattr(self.controller, name, value)
        if hasattr(self.controller, "reset_episode"):
            self.controller.reset_episode()
        self.trail.clear()

    def _draw(self):
        width, height = self.screen.get_size()
        viewport_height = height - CONTROL_HEIGHT
        cx = width / 2
        cy = viewport_height / 2 + 8
        self._draw_background(width, viewport_height, cx, cy)

        px = cx + self.rocket.x
        py = cy + self.rocket.y
        self.trail.append((int(px), int(py)))
        self.trail = self.trail[-180:]
        if len(self.trail) > 1:
            pygame.draw.lines(self.screen, "#617d94", False, self.trail, 2)

        self._draw_landing_pad(cx, cy)
        self._draw_rocket(px, py)
        self._draw_hud(width)
        self._draw_controls(width, height)

    def _draw_background(self, width, height, cx, cy):
        for y in range(height):
            ratio = y / max(height - 1, 1)
            color = (int(16 + 22 * ratio), int(24 + 35 * ratio), int(34 + 44 * ratio))
            pygame.draw.line(self.screen, color, (0, y), (width, y))

        horizon = min(int(cy + 255), height)
        pygame.draw.rect(self.screen, "#1f302c", (0, horizon, width, height - horizon))
        far = [(0, horizon + 8), (width * .14, horizon - 72), (width * .31, horizon + 16),
               (width * .47, horizon - 56), (width * .66, horizon + 10),
               (width * .83, horizon - 82), (width, horizon + 20), (width, height), (0, height)]
        near = [(0, horizon + 50), (width * .18, horizon - 18), (width * .38, horizon + 48),
                (width * .57, horizon - 26), (width * .80, horizon + 54),
                (width, horizon - 8), (width, height), (0, height)]
        pygame.draw.polygon(self.screen, "#24394b", far)
        pygame.draw.polygon(self.screen, "#2f433f", near)

        for i, size in enumerate((2, 2, 1, 2, 1, 2, 1, 2, 1)):
            x = (97 * i + 35) % max(width, 1)
            y = (53 * i + 31) % max(int(height * 0.55), 1)
            pygame.draw.circle(self.screen, "#d8e7f7", (x, y), size)

    def _draw_landing_pad(self, cx, cy):
        ground_y = int(cy + WORLD_BOTTOM)
        pygame.draw.rect(self.screen, "#101418", (int(cx - 152), ground_y - 16, 304, 26))
        pygame.draw.rect(self.screen, "#35424d", (int(cx - 150), ground_y - 14, 300, 22))
        pygame.draw.rect(self.screen, "#d2b55b", (int(cx - 58), ground_y - 22, 116, 8))

    def _draw_rocket(self, px, py):
        angle = self.rocket.angle
        body = self._rotate_points(
            [(-15, -28), (15, -28), (19, 28), (9, 38), (-9, 38), (-19, 28)], px, py, angle
        )
        nose = self._rotate_points([(0, -45), (-15, -28), (15, -28)], px, py, angle)
        left_fin = self._rotate_points([(-16, 12), (-34, 37), (-12, 32)], px, py, angle)
        right_fin = self._rotate_points([(16, 12), (34, 37), (12, 32)], px, py, angle)
        window = self._rotate_points([(-7, -15), (7, -15), (7, -1), (-7, -1)], px, py, angle)

        self._polygon(body, "#e6ecf2", "#071018", 2)
        self._polygon(nose, "#cf4f4f", "#071018", 2)
        self._polygon(left_fin, "#6689a8", "#071018", 2)
        self._polygon(right_fin, "#6689a8", "#071018", 2)
        self._polygon(window, "#8fd3ff", "#315a77", 1)
        self._draw_flames(px, py, angle)

    def _draw_flames(self, px, py, angle):
        flames = []
        if self.rocket.left_engine.isBursting():
            flames.append((-15, 38, 20, "#ffb13d"))
        if self.rocket.middle_engine.isBursting():
            flames.append((0, 42, 30, "#ffd166"))
        if self.rocket.right_engine.isBursting():
            flames.append((15, 38, 20, "#ffb13d"))

        for x_offset, y_offset, length, color in flames:
            outer = self._rotate_points(
                [(x_offset - 7, y_offset), (x_offset + 7, y_offset), (x_offset, y_offset + length)],
                px,
                py,
                angle,
            )
            inner = self._rotate_points(
                [(x_offset - 3, y_offset + 1), (x_offset + 3, y_offset + 1),
                 (x_offset, y_offset + length * .58)],
                px,
                py,
                angle,
            )
            self._polygon(outer, "#ff6f3c")
            self._polygon(inner, color)

    def _draw_hud(self, width):
        pygame.draw.rect(self.screen, "#0f151b", (14, 14, 278, 90))
        pygame.draw.rect(self.screen, "#53606d", (14, 14, 278, 90), 1)
        self._text("Mode", (28, 26), "#8da2b5", self.small_font)
        self._text("Manual" if self.manual_mode else "Q-learning", (84, 24), "#f1f6fb", self.font)
        self._engine_indicator(28, 58, "Left", self.rocket.left_engine.isBursting())
        self._engine_indicator(110, 58, "Main", self.rocket.middle_engine.isBursting())
        self._engine_indicator(192, 58, "Right", self.rocket.right_engine.isBursting())
        hint = f"Space toggles mode | G GUI | +/- speed {self.sim_speed}x"
        rendered = self.small_font.render(hint, True, pygame.Color("#c6d2df"))
        self.screen.blit(rendered, (width - rendered.get_width() - 18, 18))

    def _engine_indicator(self, x, y, label, active):
        pygame.draw.circle(self.screen, "#ffd166" if active else "#30404f", (x + 8, y + 8), 8)
        self._text(label, (x + 22, y + 1), "#dce7f3", self.small_font)

    def _draw_controls(self, width, height):
        pygame.draw.rect(self.screen, "#0e1217", (0, height - CONTROL_HEIGHT, width, CONTROL_HEIGHT))
        commands = [
            ("Pause P", self.controller.pause),
            ("Run O", self.controller.run),
            ("Explore E", self.controller.toggle_explore),
            ("Reset R", self._reset),
            ("GUI G", self.toggle_rendering),
            ("Slower -", self.speed_down),
            ("Faster +", self.speed_up),
        ]
        self.buttons = []
        x = 10
        y = height - CONTROL_HEIGHT + 7
        for label, command in commands:
            text_surface = self.small_font.render(label, True, pygame.Color("#e7edf4"))
            rect = pygame.Rect(x, y, text_surface.get_width() + 20, 28)
            color = "#314251" if rect.collidepoint(pygame.mouse.get_pos()) else "#24313c"
            pygame.draw.rect(self.screen, color, rect, border_radius=3)
            self.screen.blit(text_surface, text_surface.get_rect(center=rect.center))
            self.buttons.append((rect, command))
            x = rect.right + 6

        status = self._status_text()
        self._text(status, (12, height - 35), "#dce7f3", self.small_font)

    def _draw_silent_status(self):
        width, height = self.screen.get_size()
        self.screen.fill("#10151b")
        message = f"GUI rendering disabled. Learning continues at {self.sim_speed}x."
        rendered = self.heading_font.render(message, True, pygame.Color("#dce7f3"))
        self.screen.blit(rendered, rendered.get_rect(center=(width / 2, height / 2)))

    def _status_text(self):
        mode = "manual" if self.manual_mode else "Q-learning"
        state = "paused" if self.controller.paused else "running"
        explore = "explore" if self.controller.explore else "greedy"
        return (
            f"{state}, {mode}, {explore}, {self.sim_speed}x | "
            f"x={self.rocket.x:6.1f} y={self.rocket.y:6.1f} "
            f"vx={self.rocket.vx:6.1f} vy={self.rocket.vy:6.1f} "
            f"angle={self.rocket.angle:.3f}{self._learning_status()}"
        )

    def _learning_status(self):
        parts = []
        for name, label, format_spec in (
            ("previous_action", "action", "d"),
            ("last_reward", "reward", ".2f"),
            ("last_q_value", "q", ".2f"),
            ("last_loss", "loss", ".4f"),
            ("episode", "episode", "d"),
        ):
            value = getattr(self.controller, name, None)
            if value is not None:
                parts.append(f"{label}={value:{format_spec}}")
        replay = getattr(self.controller, "replay_buffer", None)
        if replay is not None:
            parts.append(f"replay={len(replay)}")
        if hasattr(self.controller, "qtable"):
            parts.append(f"qstates={len(self.controller.qtable)}")
        return " | " + " ".join(parts) if parts else ""

    def _text(self, text, position, color, font):
        self.screen.blit(font.render(text, True, pygame.Color(color)), position)

    @staticmethod
    def _rotate_points(points, px, py, angle):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        return [
            (px + x * cos_a - y * sin_a, py + x * sin_a + y * cos_a)
            for x, y in points
        ]

    def _polygon(self, points, fill, outline=None, width=1):
        pygame.draw.polygon(self.screen, fill, points)
        if outline:
            pygame.draw.polygon(self.screen, outline, points, width)


def main():
    SimulatorApp().run()


if __name__ == "__main__":
    main()
