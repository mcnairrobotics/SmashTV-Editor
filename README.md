# SmashTV-Editor
A level editor for the Williams Classic Smash TV

## Setup
To use this, you need to run the python script in a directory with the following rom files: \
la8_smash_tv_game_rom_u105.u105 and la8_smash_tv_game_rom_u89.u89.\
MAKE SURE YOU BACK THEM UP FIRST!\
If you have u105-la8 and u89-la8 instead, rename them to the above files.

## Entry Properties
*  Enemy: The enemy type
* Count: The total number there are
* Diff: Difficulty of the enemy. Higher difficulties typically increase speed, spawn harder variations, more projectiles, etc.
* Rate: Not exactly sure, I think it has something to do with how much they are spawned.
* Onscreen: How many start onscreen in the beginning of the level
* Counter: Not sure on this one either. I believe it's the minimum amount that has to be killed? Lower it if the game takes a while on a certain enemy.

## Running your hack
After saving your changes, run "mame smashtv" through command line or bat file. \
Make sure the files are in a folder titled Smashtv in your roms directory. \
You will know your changes worked if the game says the roms are bad.

## Warnings
* Always make a backup of your original roms. 
* Don't put more than 2 snipers in a level
* Don't start a room with 30 or more enemies, it will crash the game or skip the room.
* If an enemy is usually in a room and you set it not to be (example: mine) then the game might have an error
* If an enemy is never supposed to start in a room and it's marked too, it might crash the game
* Putting bosses in an earlier room may softlock the game because eventually weapons stop spawning
* Having too many enemies in a room at the same time might slow the game down and potentially crash it
* The cobra bosses are very glitchy

### Todo
* Figure out HTYP code that determines type for hulks, including snake hulks and mysterious unused tech crew hulk. 
* Figure out how to turn boss mutoid man into the Evil MC
* Figure out what turns normal droids to fat droids
