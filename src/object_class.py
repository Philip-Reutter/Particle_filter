import numpy as np
import pygame

from constants import WIDTH, HEIGHT, MAX_VELOCITY, FALSE_MEASUREMENT_NUMBER

class Object:
    def __init__(self, shape=None, size=30):
        self.x = np.random.uniform(0, WIDTH)
        self.y = np.random.uniform(0, HEIGHT)
        self.vx = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY)
        self.vy = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY)
        self.size = size

        self.base_noise = 5.0
        self.x_meas = None
        self.y_meas = None
        self.vx_meas = None
        self.vy_meas = None

        self.shape = shape if shape else np.random.choice(["square", "circle"])

    def move(self):
        self.x += self.vx + np.random.randn() * 0.2
        self.y += self.vy + np.random.randn() * 0.2

        if self.x < 0 or self.x > WIDTH - self.size:
            self.vx *= -1
            self.x = max(0, min(self.x, WIDTH - self.size))

        if self.y < 0 or self.y > HEIGHT - self.size:
            self.vy *= -1
            self.y = max(0, min(self.y, HEIGHT - self.size))
    
    def measurement(self):
        measurements = []

        prev_x_meas = self.x_meas
        prev_y_meas = self.y_meas
        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2

        if self.shape == "circle":
            theta = np.random.uniform(0, 2*np.pi)
            radius = np.random.randn() * (self.size / 4) # std = size/4
            self.x_meas = center_x + radius * np.cos(theta)
            self.y_meas = center_y + radius * np.sin(theta)

        elif self.shape == "square":
            self.x_meas = center_x + np.random.randn() * (self.size / 4)
            self.y_meas = center_y + np.random.randn() * (self.size / 4)

        # base noise
        self.x_meas += np.random.randn() * self.base_noise
        self.y_meas += np.random.randn() * self.base_noise

        self.vx_meas = 0.8 * self.vx_meas + 0.2 * (self.x_meas - prev_x_meas) if prev_x_meas is not None else 0
        self.vy_meas = 0.8 * self.vy_meas + 0.2 * (self.y_meas - prev_y_meas) if prev_y_meas is not None else 0

        measurements.append((self.x_meas, self.y_meas, self.vx_meas, self.vy_meas))

        # add number of false measurements per object
        for _ in range(FALSE_MEASUREMENT_NUMBER):
            x_false = np.random.uniform(0, WIDTH)
            y_false = np.random.uniform(0, HEIGHT)
            vx_false = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY)
            vy_false = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY)
            measurements.append((x_false, y_false, vx_false, vy_false))
        return measurements

    def draw(self, screen, color=(255, 0, 0)):
        if self.shape == "square":
            pygame.draw.rect(screen, color, (int(self.x), int(self.y), self.size, self.size))
        elif self.shape == "circle":
            pygame.draw.circle(screen, color, (int(self.x + self.size/2), int(self.y + self.size/2)), self.size//2)

    def draw_measurement(self, screen, measurements, color=(0, 0, 255)):
        for x_meas, y_meas, _, _ in measurements:
            if x_meas is not None and y_meas is not None:
                pygame.draw.circle(screen, color, (int(x_meas), int(y_meas)), 3)
