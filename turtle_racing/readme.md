# Turtle Racing Game

Welcome to the Turtle Racing Game! This is a fun and simple Python project that simulates a race between multiple turtles using the `turtle` graphics module. The turtles race towards the finish line, and the first one to reach the end wins!

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Customization](#customization)

## Features

- **Simple and Fun Gameplay**: Watch as turtles of different colors race to the finish line.
- **Randomized Racing**: Each turtle moves a random distance at each step, making every race unique.
- **Customizable Number of Racers**: Choose how many turtles will participate in the race (between 2 and 10).

## Installation

To run the Turtle Racing Game, you need to have Python installed on your system. You can download Python from the official [Python website](https://www.python.org/).

This game also uses the `turtle` module, which is included with Python, so no additional installations are needed.

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Shishank93774/python-projects.git
   cd turtle_racing
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```

3. **Enter the number of racers**: When prompted, enter the number of turtles that will race (between 2 and 10).

4. **Watch the race**: The race will start, and you'll see the turtles moving toward the finish line. The game will announce the winner once the race is over.

## How It Works

- The game uses the `turtle` graphics module to create a window where the race takes place.
- Each turtle is assigned a random color and positioned at the starting line.
- In each iteration of the race loop, turtles move forward by a random number of pixels.
- The first turtle to cross the finish line wins, and the game announces the winner.

## Customization

- **Window Size**: You can change the window dimensions by modifying the `WIDTH` and `HEIGHT` variables in the code.
- **Turtle Colors**: You can customize the list of colors used for the turtles by editing the `COLORS` list.
- **Race Speed**: The speed of the turtles can be adjusted by changing the range of the `step` variable in the `move` method.

