# Methodology-Faithful Reconstruction and D0 Sensitivity Analysis of Q-Learning-Based Routing in a 3D Wireless Sensor Network

## Overview

This project presents a methodology-faithful reconstruction of the Q-learning-based routing approach described in the reference paper:

> **Q-learning-based Optimization of Smart Home's Wireless Sensors Network Lifetime**

The implementation evaluates energy-aware routing in a reconstructed 45-node 3D Wireless Sensor Network (WSN) and performs an additional experimental extension through **D0 sensitivity analysis**.

The project includes the reconstructed Q-learning implementation, Dijkstra baseline, energy-model validation, experimental results, visualizations, research paper, and presentation.

---

## Reference Paper

**Title:**  
Q-learning-based Optimization of Smart Home's Wireless Sensors Network Lifetime

**Authors:**

- Ismael Jrhilifa
- Hamid Ouadi
- Abdelilah Jilbab

**Journal:**  
International Journal of Renewable Energy Research (IJRER)

**Volume:** 13  
**Issue:** 1  
**Publication:** March 2023  
**Pages:** 302–310

**DOI:**  
10.20508/ijrer.v13i1.13684.g8684

**Official Paper:**  
https://ijrer.org/index.php/ijrer/article/view/13684

---

## Objectives

The project aims to:

1. Reconstruct the main Q-learning-based routing methodology from the reference paper.
2. Implement the first-order radio energy model.
3. Implement the paper-based reward and path-quality calculations.
4. Perform energy-aware candidate route selection.
5. Implement a Dijkstra shortest-path baseline.
6. Validate complete-path energy feasibility.
7. Evaluate the reconstructed 45-node 3D network.
8. Extend the experiment through D0 sensitivity analysis.

---

## Network Configuration

| Parameter | Value |
|---|---:|
| Total nodes | 45 |
| Sensor nodes | 44 |
| Sink | 1 |
| Deployment area | 16 × 13 × 2.5 m |
| Initial sensor energy | 0.5 J |
| Packet size | 512 bits |
| E_ELEC | 5 × 10⁻⁸ J/bit |
| E_AMP | 1 × 10⁻¹⁰ J/bit/m² |
| Coordinate seed | 42 |
| Communication range | 7.0 m |
| Baseline D0 | 4.0 m |
| Maximum stored paths/source | 20 |
| Maximum routing hops | 6 |

### Reconstruction Assumptions

The complete original node-coordinate dataset and some simulation details were not available.

Therefore:

- Sensor coordinates were reconstructed within the reported deployment area using seed 42.
- A 7.0 m communication range was used to construct the communication graph.
- D0 = 4.0 m was used as the baseline propagation-threshold assumption.

These values are **implementation assumptions** and are not claimed to be numerical parameters directly provided by the reference paper.

---

## Methodology

### 1. 3D Network Construction

A 45-node 3D wireless sensor network is reconstructed using the reported deployment dimensions.

The Sink is positioned at: (8.0, 6.5, 0)



----
Author
**Syeda Nishat**
Reinforcement Learning Research Project

45-Node 3D Wireless Sensor Network
Q-Learning Routing Reconstruction and Experimental Extension
