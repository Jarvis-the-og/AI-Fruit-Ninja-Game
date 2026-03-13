# AI Fruit Ninja – Hand Gesture Game

A Python-based **Fruit Ninja style game controlled using hand gestures**.
The game uses computer vision to track the player's hand through a webcam and allows slicing fruits using the **index finger as a blade**.

## Features

* Real-time **hand tracking using MediaPipe**
* **Webcam-based gesture control**
* Fruits spawn randomly and fall on the screen
* Slice fruits by moving your finger across them
* Score counter

## Tech Stack

* Python
* OpenCV
* MediaPipe
* Pygame
* NumPy

---

# Project Structure

```
AI-Fruit-Ninja-Game
│
├── main.py              # Main game loop
├── hand_tracking.py     # Hand detection using MediaPipe
├── fruit.py             # Fruit object logic
├── assets/              # Images and assets
└── README.md
```

---

# Installation

## 1. Clone the repository

```
git clone https://github.com/Jarvis-the-og/AI-Fruit-Ninja-Game.git
cd AI-Fruit-Ninja-Game
```

## 2. Install Python dependencies

```
pip install pygame opencv-python mediapipe numpy
```

---

# Run the Game

```
python main.py
```

Two windows will appear:

1. Webcam window showing hand tracking
2. Game window where fruits fall

Move your **index finger** to slice fruits.

---

# Requirements

* Python 3.10 / 3.11 recommended
* Webcam
* Windows / Linux / Mac

---

# How It Works

1. Webcam captures real-time video
2. MediaPipe detects hand landmarks
3. Index finger coordinates are tracked
4. Finger movement acts as a blade
5. Collision detection slices fruits

---

# Contributing

Contributions are welcome!

### Steps to contribute

1. Fork the repository
2. Create a new branch

```
git checkout -b feature-name
```

3. Make your changes
4. Commit your changes

```
git commit -m "Add new feature"
```

5. Push the branch

```
git push origin feature-name
```

6. Open a Pull Request

---

# Possible Improvements

* Add fruit slicing animation
* Add bombs
* Add sound effects
* Add difficulty levels
* Add multiplayer gesture control

---

# License

This project is open-source and available under the MIT License.
