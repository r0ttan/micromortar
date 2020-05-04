Friendly virtual mortar battle game for bbc micro:bit.

By Tobias Gustavsson
written in Micropython.

Install instructions:

Requires two micro:bits within radio range of each other.
Goto https://python.microbit.org/v/1.1
Load micromortar.py into editor.
Download micromortar.hex
Transfer .hex to your micro:bit

GLHF



How to play.

Upon start of the micro:bit it will listen and send suggestion of a randomly chosen virtual distance between the two micro mortars. When distance is negotiated a short countdown will start the match.

Choose angle by tilting the micro:bit around the y-axis. Holding it parallell to the ground with leds facing up equals zero degrees, keeping it vertical with the ground means 90 degrees. Both values are not a good choice, the mortar does have self destruction protection, you can not hit yourself. When desired angle is set, hold button A to set velocity of projectile (1-5). Release button A, display will flash F two times before projectile is launched. Display will show if the shot was too long or short, or if it was a hit. The game will end when you hit the opponent or the opponent hits you. Press button B to forfeit the game, this will render the oppontent winner.