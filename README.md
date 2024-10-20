# SyntaxError2024

This is a simple game project of team "AI ki waifu" for the hackathon Syntax Error 2024 organized by the Indian Institute of Technology Roorkee.
We built a simple building defence game in `pygame` and an Arduino Uno R3 based controller for the game.

This is a Python-based game built using Pygame and PySerial, featuring randomly generated terrain and A* (A-Star) pathfinding.

You can find the video link in this drive
## Video Link
https://drive.google.com/drive/folders/1Wu7UtgHDRqxQ14V49FrwtmtRKda_qlHb

## Features
- Randomly Generated Terrain: Each game session generates a new map with random obstacles, ensuring that gameplay remains dynamic. It generates stones, ponds and plains at randomly, while at the same time ensures that the centre area has always some play area.
- Made a custom textures for terrain.
- A Pathfinding Algorithm:* Enemies use the A* algorithm to find the shortest path to the centre, navigating around obstacles.
- Guaranteed Path: The game guarantees that enemies always reach the centre using intelligent pathfinding, ensuring the game remains fair and functional.
- PySerial Integration: Game logic utilizes PySerial, enabling potential interactions with a custom-made Arduino Uno R3 Controller.

## Installation
1. First clone the repository and go to the main directory
```bash
git clone https://github.com/ManjotSingh08x/SyntaxError2024.git
cd SyntaxError2024/SyntaxError2024/
```
2. Install requirements
```bash
pip install -r requirements.txt
```
or 
```bash
python -m pip install -r requirements.txt
```
3. Run the main game file
```bash
python main.py
```
4. Enjoy!

## Team Members

Taufeeque, Manjot, Siddharth, Manhar
