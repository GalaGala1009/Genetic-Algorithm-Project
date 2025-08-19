# Genetic Algorithm Ball Simulation

A visual simulation that demonstrates genetic algorithms through balls that evolve to collect food efficiently.

## Overview

This project implements a genetic algorithm simulation where balls evolve over generations to better collect food particles. Each ball has a genetic code that determines its properties:

- Size (7 bits)
- Speed (3 bits) 
- Color (24 bits)

![balls](./img/balls.gif)

## Features

- Balls move around in a canvas environment
- Food particles randomly spawn with different colors
- Balls collect food and gain scores based on:
  - Color matching (better matches = higher scores)
  - Food's remaining life
- Genetic evolution through:
  - Crossover between top performing balls
  - Random mutations
  - Natural selection based on performance

### Ball Properties
- Each ball has:
  - Position (x, y)
  - Direction vectors (dx, dy)
  - Size (radius)
  - Color
  - Life span
  - Score

### Evolution Parameters
- Initial mutation rate: 0.2 
- Mutation rate decreases every 5000 frames
- New offspring generated every 2500-5000 frames
- Parent selection from top 4 performing balls

### Physics
- Ball-to-ball collision detection and response
- Wall collision detection and bouncing
- Velocity normalization to maintain consistent speeds

## Visualization

- Real-time ranking display showing:
  - Ball colors
  - Performance scores
  - Genetic codes
- Mating log showing parent and child colors
- Time and frame counter

## Usage

1. Open `index.html` in a web browser
2. Watch the balls evolve as they collect food
3. Monitor performance in the ranking panel
4. Observe genetic inheritance through the mating log

## Requirements

- Modern web browser with HTML5 Canvas support
- No additional dependencies required