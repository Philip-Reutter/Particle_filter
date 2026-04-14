# Particle Tracking & Clustering Simulation

A real-time 2D simulation that explores object tracking under noisy measurements using particle filtering, clustering, and temporal smoothing.

---

## Overview

This project simulates multiple moving objects in a noisy environment and tracks them over time using a probabilistic particle filter. Measurements are intentionally noisy, requiring robust clustering and temporal tracking.

Objects are not directly observed. Instead, the system estimates their positions from noisy measurements using weighted particles and groups observations using DBSCAN clustering.

---

## Features

- Noisy synthetic sensor measurements
- Particle filter for probabilistic state estimation
- DBSCAN clustering for detection grouping
- Track management with motion prediction
- Simple shape-based feature extraction (covariance eigenvalue ratio)
- Temporal smoothing for more stable tracking

---

## Controls

- SPACE → Pause / Resume
- RIGHT ARROW → Step frame
- O → Toggle objects
- P → Toggle particles
- M → Toggle measurements
- C → Toggle cluster display

---

## Installation

### Conda (recommended)

```bash
conda env create -f environment.yml
conda activate particle-filter
```

### Run

```bash
python src/main.py
```

---

## Dependencies

- Python 3.12
- NumPy
- SciPy
- scikit-learn
- pygame

---

## Visualization

### Demo

![Demo](assets/demo.gif)

---

## Status

⚠️ Work in progress

The tracking and clustering pipeline is functional but still being refined, especially in terms of classification stability under noisy conditions.

---

Built as an experimental project for exploring and visualizing particle filtering and multi-object tracking.
