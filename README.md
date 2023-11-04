# space-station-simulation
Desktop simulation of alien invasion on space station written in PyGame.

## Description of the simulation
This app is meant to demonstrate threads competing for limited resources:
- Station is continuously attacked by aliens
- Aliens approach the nearest astronaut do contact damage
- Aliens are killed by astronauts, but they have limited ammo
- If an astronaut is out of ammo, he has to go into armory
- **Only two astrunauts can be in the armory at a given time**
- If an astronaut's health points fall below 50%, he has to go to medical room
- **Only one astronaut can be inside medical room at a given time**
- Queuing for medical & armory is handled using threads
- If astronauts's health point fall to 0, he dies
- If all astrounats die, aliens win and the simulation is over

## Requirements
In order to run the simulation you need install PyGame. 
Then, start the app using this command:
```
python run.py
```

## Screenshots
<img width="1275" alt="image" src="https://github.com/Droniu/space-station-simulation/assets/41952692/b0dad8f6-ad48-413e-a528-3a8325b2d32e">
