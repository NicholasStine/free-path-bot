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