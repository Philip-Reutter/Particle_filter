from sklearn.cluster import DBSCAN
import numpy as np

def dbscan_clustering(particles, eps = 20, min_samples = 40):
    positions = np.array([[p.x, p.y] for p in particles])
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(positions)
    labels = db.labels_

    cluster_centers = []
    cluster_shapes = []

    for label in set(labels):
        if label == -1:
            continue # skip noise
        cluster_points = positions[labels == label]
        center = cluster_points.mean(axis=0)
        cluster_centers.append(center)

        # covariance
        cov = np.cov(cluster_points.T)

        eigvals, eigvecs = np.linalg.eig(cov)

        # sort
        idx = np.argsort(eigvals)[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]

        ratio = eigvals[0] / (eigvals[1] + 1e-6)

        cluster_shapes.append({
            "center": center,
            #"eigvals": eigvals,
            #"eigvecs": eigvecs,
            "ratio": ratio,
        })

    return cluster_centers, cluster_shapes
