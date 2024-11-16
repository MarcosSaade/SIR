# SIR Model Simulation Using Pygame and Python

A project on computational epidemiology, differential modeling, and the visual simulation of dynamic systems.

![image](https://github.com/user-attachments/assets/bdb7f716-fc56-46b9-9392-54dca1e74bb4)

## Overview
This project demonstrates a dynamic simulation of the SIR (Susceptible-Infected-Recovered) model, commonly used to describe the spread of infectious diseases. Developed as part of a university course on differential equations, the simulation leverages Python and Pygame to visualize how stochastic interactions influence disease transmission. The project also provides graphical insights into the behavior of the system over time using Matplotlib.

Key aspects include modeling systems of differential equations and incorporating stochastic behaviors to reflect real-world complexities in disease spread.

## Features
- **Interactive Simulation**: Individuals are represented as moving agents whose states are color-coded (susceptible, infected, or recovered). Their interactions are simulated in real time, capturing the stochastic nature of disease transmission.
- **Dynamic State Transitions**: State changes occur based on defined interaction rules, allowing susceptible individuals to become infected upon contact and infected individuals to recover over time. These transitions are governed by differential equations to represent infection rates and recovery.
- **Graphical Analysis**: The evolution of the SIR model is plotted using Matplotlib, providing a clear visualization of how the population moves between susceptible, infected, and recovered states over time.

![image](https://github.com/user-attachments/assets/58ddd97e-0633-4d56-98c9-6d54e9bd1d60)

## Requirements
- Python 3.x
- Pygame
- NumPy
- Matplotlib

## Installation
1. Ensure Python 3.x is installed.
2. Install the required libraries by running:
   ```bash
   pip install pygame numpy matplotlib
   python3 main.py
   ```
