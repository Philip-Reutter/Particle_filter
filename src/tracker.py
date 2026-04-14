import numpy as np

def classify_ratio(r):
    if r < 2.5:
        return "circle"
    elif r < 6.0:
        return "square"
    else:
        return "noise"

class Track:
    def __init__(self, track_id, center):
        self.id = track_id
        self.center = center
        self.velocity = np.array([0.0, 0.0])
        self.age = 0              # frames since last seen
        self.hits = 1             # times matched
        self.ratio = 0.0
        self.label_history = []
        self.label = "unknown"

class Tracker:
    def __init__(self, max_age=40, dist_threshold=50):
        self.tracks = []
        self.next_id = 0
        self.max_age = max_age
        self.dist_threshold = dist_threshold

    def update(self, cluster_shapes):
        new_tracks = []

        # predict positions
        preds = [t.center + t.velocity for t in self.tracks]

        # match clusters to tracks
        used_tracks = set()

        for c in cluster_shapes:
            center = c["center"]

            # find best match
            best_idx = None
            best_dist = float("inf")

            for i, t in enumerate(self.tracks):
                if i in used_tracks:
                    continue
                pred = preds[i]
                dist = np.linalg.norm(center - pred)

                if dist < best_dist:
                    best_dist = dist
                    best_idx = i

            if best_idx is not None and best_dist < self.dist_threshold:
                # match found
                t = self.tracks[best_idx]
                used_tracks.add(best_idx)

                # update velocity
                new_velocity = center - t.center
                t.velocity = 0.7 * t.velocity + 0.3 * new_velocity

                # update position
                t.center = center
                t.age = 0
                t.hits += 1

                alpha = 0.1

                if t.hits == 1:
                    t.ratio = c["ratio"]
                else:
                    t.ratio = (1 - alpha) * t.ratio + alpha * c["ratio"]

                label = classify_ratio(t.ratio)
                t.label_history.append(label)

                if len(t.label_history) > 10:
                    t.label_history.pop(0)

                final_label = max(set(t.label_history), key=t.label_history.count)
                t.label = final_label

                new_tracks.append(t)

            else:
                t = Track(self.next_id, center) # new track
                t.ratio = c["ratio"]
                self.next_id += 1
                new_tracks.append(t)

        # keep unmatched old tracks (for crossing objects)
        for i, t in enumerate(self.tracks):
            if i not in used_tracks:
                t.age += 1

                if t.age < self.max_age:
                    t.center = t.center + t.velocity
                    new_tracks.append(t)

        self.tracks = new_tracks

        return self.tracks
