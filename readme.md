# Free Path Bot

## Overview
This project started with the goal of training an unsupervised Policy Gradient Network to drive a car around a 2D track with only 3 distance sensors at 0 degrees (forward), 45 degrees, and -45 degrees. For anyone who knows anything about neural networks, you probably could have told me that this was a tremendous waste of time, but I'm glad nontheless that I wasted that time myself!

The project has now transformed into it's *final form*. It's a 2D racing game built in pygame where you can plug in any one of 3 available Agents (PGN, FCN, and SillyGoose) to make realtime gas, brake, and steering decisions based on the current game state. There's also a joystick class for driving the car with the arrow keys, the map class which can accept any of the .jpg image names in the /images directory, and a checkpoint class that allows for drawing checkpoints, but it may or may not be broken...

## Instructions

### Install
1. clone this repo (duh)
2. cd into the cloned repo
3. install the packages. *You should probably use anaconda or some other virtual environment.. or don't, it's your life. Tbh, neither do I, I just make a mess of the packages installed on my os hehehe*
```
pip install --user tensorflow pygame numpy
```
4. run the game and training loop with
```
python main.py
```
5. deal with the almost certain flow of "package not found" errors :)
6. keep trying till it works..?
7. throw your keyboard and / or computer into a lake

## OGM
### *Occupancy Grid Mapping*
So this is cool! One of the great mysteries of my childhood was how a roomba can map it's way around a room using lasers? I think I read in a popular science edition that they make a map with these laser scans to decide where and how to best vacuum the room. I was prompthing Grok for "how can I use my existing laser scanner and 2D car simulation to 'map' the track" when I stumbled upon two very fascinating pieces of tech. Firstly to catch my eye was OGM. You could use some weird logarithmic magic to build a down sampled grid like representation of where the car can drive and where it can't. Super cool! I also upgraded from a fixed laser scanner on the front of the car to a pseudo-lidar implementation with lasers at fixed increments of 3 degrees (more resolution would be better but my laptop is S&%T so what'cha gonna do?). This gives me a really cool grayscale representation of the environment, and with a little scipy and numpy magic, I managed to use dilation and erosion to denoise and delineate the track, boundaries, and occupied space. I can then draw them in white, red, and black respectively, to produce a plot where the track and edges are color coded and clearly visible. I can also subtrack the edges from the track, to produce a black and white image where the white pixels are a safe-driving zone, and everythine else (including the dilated area around the borders) is shown as black for occupied. Que interesante!-