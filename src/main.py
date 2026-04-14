import pygame

from particle_class import Particle
from object_class import Object
from constants import *
from clustering import dbscan_clustering
from tracker import Tracker

tracker = Tracker()
particles = [Particle(1/N_PARTICLES) for _ in range(N_PARTICLES)]
objects = [Object() for _ in range(N_OBJECTS)]
all_measurements = []
cluster_centers = []
cluster_shapes = []
tracks = []

#for i in range (10):
#    print(particles[i])

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

running = True
paused = True
step = False
show_objects = True
show_measurements = True
show_particles = True
show_clusters = False

while running:
    screen.fill((0, 0, 0))

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Pause / Resume
                paused = not paused
            elif event.key == pygame.K_RIGHT: # Step one frame
                step = True
            elif event.key == pygame.K_o:  # Toggle objects
                show_objects = not show_objects
            elif event.key == pygame.K_m:  # Toggle objects
                show_measurements = not show_measurements
            elif event.key == pygame.K_p:  # Toggle particles
                show_particles = not show_particles
            elif event.key == pygame.K_c:  # Toggle cluster centers
                show_clusters = not show_clusters

    if not paused or step:
        all_measurements = []
        # Movement and measurement
        for o in objects:
            o.move()
            measurements = o.measurement()
            all_measurements.extend(measurements)

        for p in particles:
            p.update_by_prediction()
            p.update_by_measurement(all_measurements)
        particles = Particle.resample_particles(particles, objects)
        cluster_centers, cluster_shapes = dbscan_clustering(particles)
        tracks = tracker.update(cluster_shapes)
        print(cluster_shapes)

    # Draw
    for o in objects:
        if show_objects:
            o.draw(screen)
        if show_measurements:
            o.draw_measurement(screen, all_measurements)
        
    for p in particles:
        if show_particles:
            p.draw(screen)
    
    for t in tracks:
        if t.age > 2 or not show_clusters:
            continue
        x, y = int(t.center[0]), int(t.center[1])

        # draw circle
        pygame.draw.circle(screen, (0, 255, 255), (x, y), 15, 2)

        label = t.label

        text = f"ID {t.id} | {label}"
        img = font.render(text, True, (255, 255, 255))
        screen.blit(img, (x + 10, y + 10))

    pygame.display.flip()
    clock.tick(60)
    if step:
        step = False

pygame.quit()
