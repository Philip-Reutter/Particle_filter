import numpy as np
import pygame
import copy

from constants import WIDTH, HEIGHT, MAX_VELOCITY, MOVE_TO_MEASUREMENT_SPEED, RESAMPLE_RATIO, EXPLORATION_RATIO

class Particle:
    def __init__(self, weight):
        self.weight = weight
        self.x = np.random.uniform(0, WIDTH)
        self.y = np.random.uniform(0, HEIGHT)
        self.vx = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY)
        self.vy = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY)

    def __str__(self):
        return f"Particle at ({self.x}, {self.y}) with velocity ({self.vx}, {self.vy}) and weight {self.weight}"
    
    def update_by_prediction(self):
        self.x += self.vx + np.random.randn() * 2
        self.y += self.vy + np.random.randn() * 2
        self.vx += np.random.randn() * 0.1
        self.vy += np.random.randn() * 0.1

    def update_by_measurement(self, measurements):
        smallest_dist = np.sqrt(WIDTH**2 + HEIGHT**2 + 2 * MAX_VELOCITY**2)
        object_index = None
        for i, (x_meas, y_meas, vx_meas, vy_meas) in enumerate(measurements):
            if x_meas is not None and y_meas is not None:
                dx = self.x - x_meas
                dy = self.y - y_meas
                dvx = self.vx - vx_meas
                dvy = self.vy - vy_meas
                dist = np.sqrt(dx**2 + dy**2 + dvx**2 + dvy**2)
                if dist < smallest_dist:
                    smallest_dist = dist
                    object_index = i
        if object_index is not None:
            x_meas, y_meas, vx_meas, vy_meas = measurements[object_index]
            self.x += (x_meas -self.x) * MOVE_TO_MEASUREMENT_SPEED
            self.y += (y_meas -self.y) * MOVE_TO_MEASUREMENT_SPEED
            self.vx += (vx_meas -self.vx) * MOVE_TO_MEASUREMENT_SPEED
            self.vy += (vy_meas -self.vy) * MOVE_TO_MEASUREMENT_SPEED

            sigma_pos = 9.0
            sigma_vel = 4.0
            self.weight = np.exp(-(dx**2 + dy**2)/(2*sigma_pos**2)) \
                    * np.exp(-(dvx**2 + dvy**2)/(2*sigma_vel**2))
            self.weight = max(self.weight, 1e-300)

    def draw(self, screen, color = (255, 255, 0)):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 1)

    @staticmethod
    def resample_particles(particles, objects):
        N = len(particles)
        # normalize weights
        weights = np.array([p.weight for p in particles])
        weights /= np.sum(weights)
        for p, w in zip(particles, weights):
            p.weight = w

        new_particles = particles.copy()
        # resample indices
        n_resample = int(N * RESAMPLE_RATIO)
        resample_sources = np.random.choice(N, size=n_resample, p=weights)
        resample_targets = np.random.choice(N, size=n_resample, replace=False)

        for src_idx, tgt_idx in zip(resample_sources, resample_targets):
            new_particles[tgt_idx] = copy.deepcopy(particles[src_idx])
            p = new_particles[tgt_idx]
            p.x += np.random.randn() * 2
            p.y += np.random.randn() * 2
            p.vx += np.random.randn() * 0.2
            p.vy += np.random.randn() * 0.2

        # distribute some particles randomly on measurement positions
        n_explore = int(N * EXPLORATION_RATIO)
        particles_per_object = n_explore // len(objects)
        explore_targets = np.random.choice(N, size=n_explore, replace=False)
        explore_idx = 0

        for obj in objects:
            if obj.x_meas is None or obj.y_meas is None:
                continue
            for _ in range(particles_per_object):
                if explore_idx >= n_explore:
                    break

                tgt_idx = explore_targets[explore_idx]
                p = new_particles[tgt_idx]
                p.x = obj.x_meas + np.random.randn() * 2
                p.y = obj.y_meas + np.random.randn() * 2
                p.vx = obj.vx_meas + np.random.randn() * 0.2
                p.vy = obj.vy_meas + np.random.randn() * 0.2

                explore_idx += 1

        for p in new_particles:
            p.weight = 1.0 / N

        return new_particles
