# pysimpleclicker
simple tool for emulating interactive user actions

#### EN [RU](READMEru.md)

It can work with road steps from a file. Steps can be of 3 types: push the keyboard, clicking on the image on the screen and waiting for the image on the screen.

Options must be in JSON format and have list (array) of steps with properties:
* type ( | PushKeyboard | WaitForImage | ClickToImg | )
* value (key name for first type, and path to image for another types)
* count (for type WaitForImage it is max repeat count)
* delay (in ms before next repeat)
* sleep (in ms after current step before next step)