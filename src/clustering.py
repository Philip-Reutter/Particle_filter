from sklearn.cluster import DBSCAN
import numpy as np

def dbscan_clustering(particles, eps = 20, min_samples = 40):
    positions = np.array([[p.x, p.y] for p in particles])
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(positions)
    labels = db.labels_
    cluster_centers = []
    for label in set(labels):
        if label == -1:
            continue  # skip noise
        cluster_points = positions[labels == label]
        center = cluster_points.mean(axis=0)  # mean x and y
        cluster_centers.append(center)

    return cluster_centers
