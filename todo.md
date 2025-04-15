module for pickling observations
 - mainly for not having to run the game and drive around every time I'm working on OGM or other env mapping ops
 - this should be the only place that I check for cli args regarding clearing pickled data
 - could support different schemas?


Go back to genetic FCN with lidar data?
 - start with fixed?
 - maybe I init the lidar and network together so I can dynamically set number of nodes
 - I should be saving the w&b's ot avoid having to train the network every time


Let's go back to rendering multiple agents at once
 - can I make it compatible with the current observation schema
 - if so, this would be used as a post-processor to generate a more useful visual of learning progress & agent behavior.


I should move the different plotting configs 
 - track and borders, safe area, anything ellsssseeeee...?
 - should I have a wrapper function that defaults to probably track and borders


draw the OGM in pygame, not pyplot
 - it needs reworking to run in real time (i.e. to run in the game loop)
 - can I have different CLI args for different plot configs? 
   - I don't think I'd have to use args since cli args are in the global scope
 - I may run into issues with the grid overflowing along the width axis


can I add in a PID?
 - I would want to update the simulation to make driving more realistic, with...
   - momentum
   - drifting?
   - better modeling of turn radius (r) as a function:
     - r = f(v,b)
     - v: velocity (continuous, float)
     - b: braking (binary)
 - it would only be useful when using path finding algos (or ai?) to find a way around the track
 - it would live in the car I think? I believe that's where most telemetry data lives, so it would fit right in


path finding to replace neural networks
 - A* probably?
 - I would use it on the safe area plot
 - would this be used durring or after environment exploration?


can I use a CNN on the OGM grid representation learn to drive?
 - just like heuristic path finding, would I use this during or after exploration?
 - 

starting points! starting points, starting points!! starting points!!!!
 - I want a sandbox environment to select starting positions.
 - positions would include pos and theta
 - saves a pickled list of positions for use in the main game loop
 - would this live in the car?
 - the UX/UI would work as follows:
   1. start the sandbox environment and init and empty position list
   2. move the mouse to a desired starting position
   3. click and hold to set the position
   4. drag the cursor up or down to set the theta
   5. release the mouse to add position and theta to the position list
   6. check for x button press, if found: jump to step 8
   7. repeat from step 2
   8. pickle the position list
   9. quit pygame


can I go back to the checkpoints module?
 - what if I were to set checkpoints on the OGM grid, and not the map itself?
 - I would like to work this into a web based UX/UI with:
   - checkpoints mode!!
	    my original inspiration for the mobile UX/UI is so that if and when I switch to a physical bot, 
        I can use my phone to select desired checkpoints after the car has done some exploration. That
        way it has a defined path to follow and it's not just driving around at random.
   - exploration mode
     - the car drives around on it's own, probably with a heuristic model
     - an OGM and the car's position are displayed and updated in real time
     - this OGM should automatically scale to the current size of the explored env
   - training mode
     - I display the training on the web page :) 
     - generation and population dropdowns for the training loop
     - a pre-trained model selection dropdown for choosing a starting w&b file (should load options from saved files..? or database?)
     - an agent selection dropdown, with options for FCN and PPO
     - a data selection dropdown for OGM, lidar, or scanner
     - a display style dropdown for OGM, real-time, or full map
   - driving mode
     - a single agent does it's darndest to drive around the track
     - every time that bad boy crashes, a new one starts, and the loop repeats!
     - an agent selection dropdown, with options for 
       - FCN
       - PPO
       - SillyGoose
       - A*
     - display select dropdown for ogm, rt, fm MOVE TO ALWAYS
     - display current score?
     - reward function!! I need to start tracking changes to my reward functions 
       so I can go back and forth between different attempts without rewrites
