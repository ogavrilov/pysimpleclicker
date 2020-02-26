# pysimpleclicker
simple tool for emulating interactive user actions

#### EN [RU](READMEru.md)

Options must be in JSON format and have list (array) of steps with properties, for example:

##### WaitForImage
Wait until the image appears on the screen.
````json
[
  {
    "type": "WaitForImage",
    "value": "/path/to/img",
    "count": 5,
    "sleep": 3000,
    "delay": 150
  }
]
````
The block above means that the algorithm will wait for the image to appear on the screen along the way /path/to/img 5 times with a pause of  3 seconds (3000 ms), and after the appearance will go to the next step in 0.15 a fraction of a second (150 ms).
If the image is not found, the algorithm will wait 3 seconds before each next attempt (it is also worth considering that the time to determine the presence of the image on the screen in this case is not taken into account.

##### ClickToImg (left button)
Click to the image on the screen.
````json
[
  {
    "type": "ClickToImg",
    "value": "/path/to/img",
    "count": 2,
    "sleep": 250,
    "delay": 150
  }
]
````
The above block means that the algorithm will search for the image on the screen along the path /path/to/img and if successful, double-click on the center of this image with a pause of 0.25 seconds (250 ms) after each click, and then proceeds to the next step in 0.15 fractions of a second (150 ms).

##### RightClickToImg (right button)
similar to the blocks above
##### PushKeyboard
Press key (key down and instantly key up)
````json
[
  {
    "type": "PushKeyboard",
    "value": "a",
    "count": 3,
    "sleep": 100,
    "delay": 150
  },
  {
    "type": "PushKeyboard",
    "value": "enter",
    "count": 1,
    "sleep": 100,
    "delay": 150
  },
  {
    "type": "PushKeyboard",
    "value": ["shift", "a"],
    "count": 3,
    "sleep": 100,
    "delay": 150
  }
]
````
The above blocks means that the algorithm will press the keyboard button three times 'a' with a pause of 0.1 second, wait 0.15 seconds, press Enter once, wait 0.15 seconds and press and release the Shift button three times in succession and 'a' in the specified order.

##### KeyDown
similar to the blocks above
##### KeyUp
similar to the blocks above
##### WriteText
similar to the blocks above

