import time
import pyautogui
import os
import json
import sys

class pySimpleClicker:

	def __init__(self, actions):
		self.errorFlag = False
		self.textLog = ''
		self.actions = actions

	def __executeActionTypeWaitFoImg(self, imgPath, repeatCount, repeatDelay, endDelay):
		haveDone = False
		self.textLog += '\n\tWaiting for image by pattern: ' + imgPath
		for i in range(0, repeatCount):
			points = pyautogui.locateCenterOnScreen(imgPath)
			if points != None:
				self.textLog += '\n\tImage found at ' + str(i+1) + ' iterations with delay of ' + str(i*repeatDelay) + ' ms'
				haveDone = True
				break
			elif i < repeatCount and repeatDelay > 0:
				time.sleep(repeatDelay)
		if haveDone:
			if endDelay > 0:
				time.sleep(endDelay)
		else:
			self.textLog += '\nError: image not found by pattern: ' + imgPath + ' after ' + str(repeatCount) + ' wait iterations with delay of ' + str(repeatCount*repeatDelay) + ' ms'
			self.errorFlag = True
		return points

	def __executeActionTypeClickToImg(self, imgPath, repeatCount, repeatDelay, endDelay, buttonLeft=True):
		textLog = '\n\tLeft click by Image (by pattern: ' + imgPath + ')'
		points = self.__executeActionTypeWaitFoImg(imgPath, repeatCount, repeatDelay, endDelay)
		if self.errorFlag == False:
			pyautogui.moveTo(points.x, points.y)
			for i in range(0, repeatCount):
				if buttonLeft:
					pyautogui.click()
					textLog += ' left button'
				else:
					pyautogui.rightClick()
					textLog += ' right button'
				self.textLog += textLog
				if i < repeatCount and repeatDelay > 0:
					time.sleep(repeatDelay)
			if endDelay > 0:
				time.sleep(endDelay)

	def __executePushKeyboard(selfself, keyValue):
		if type(keyValue) == str:
			pyautogui.keyDown(keyValue)
			pyautogui.keyUp(keyValue)
		elif type(keyValue) == list:
			for keyValueStr in keyValue:
				pyautogui.keyDown(keyValueStr)
			for keyValueStr in keyValue:
				pyautogui.keyUp(keyValueStr)

	def __executeActionTypePushKeyboard(self, keyValue, repeatCount, repeatDelay, endDelay):
		for i in range(0, repeatCount):
			self.__executePushKeyboard(keyValue)
			self.textLog += '\n\tPush key "' + keyValue + '"'
			if i < repeatCount and repeatDelay > 0:
				time.sleep(repeatDelay)
		if endDelay > 0:
			time.sleep(endDelay)

	def __executeActionTypeKey(self, keyValue, repeatCount, repeatDelay, endDelay, keyDown=True):
		for i in range(0, repeatCount):
			if keyDown:
				pyautogui.keyDown(keyValue)
				self.textLog += '\n\tKey down "' + keyValue + '"'
			else:
				pyautogui.keyUp(keyValue)
				self.textLog += '\n\tKey up "' + keyValue + '"'
			if i < repeatCount and repeatDelay > 0:
				time.sleep(repeatDelay)
		if endDelay > 0:
			time.sleep(endDelay)

	def __executeActionTypeText(self, keyValue, repeatCount, repeatDelay, endDelay):
		for i in range(0, repeatCount):
			pyautogui.write(keyValue)
			self.textLog += '\n\tWrite text: "' + keyValue + '"'
			if i < repeatCount and repeatDelay > 0:
				time.sleep(repeatDelay)
		if endDelay > 0:
			time.sleep(endDelay)

	def executeActions(self):
		for action in self.actions:
			curTextError = ''
			# prepare action values
			actionType = action.get('type', '').lower()
			actionValue = action.get('value', '')
			actionCount = int(action.get('count', 0))
			actionSleep = int(action.get('sleep', 0)) / 1000
			actionDelay = int(action.get('delay', 0)) / 1000
			# log
			self.textLog += '\nAction |type:' + actionType + '|value:' + actionValue + '|count:' + str(actionCount) + '|sleep:' + str(actionSleep) + '|delay:' + str(actionDelay) + '|'
			# check action values
			if actionType == '':
				curTextError += 'Type incorrect;'
			if actionValue == '':
				curTextError += 'Value incorrect;'
			if self.errorFlag == False:
				if actionType == 'ClickToImg'.lower():
					self.__executeActionTypeClickToImg(actionValue, actionCount, actionDelay, actionSleep)
				elif actionType == 'RightClickToImg'.lower():
					self.__executeActionTypeClickToImg(actionValue, actionCount, actionDelay, actionSleep, buttonLeft=False)
				elif actionType == 'PushKeyboard'.lower():
					self.__executeActionTypePushKeyboard(actionValue, actionCount, actionDelay, actionSleep)
				elif actionType == 'KeyDown'.lower():
					self.__executeActionTypeKey(actionValue, actionCount, actionDelay, actionSleep)
				elif actionType == 'KeyUp'.lower():
					self.__executeActionTypeKey(actionValue, actionCount, actionDelay, actionSleep, keyDown=False)
				elif actionType == 'WriteText'.lower():
					self.__executeActionTypeText(actionValue, actionCount, actionDelay, actionSleep)
				elif actionType == 'WaitForImage'.lower():
					self.__executeActionTypeWaitFoImg(actionValue, actionCount, actionDelay, actionSleep)
			if self.errorFlag == True:
				break

# parse argv and get dict {key = value}
def getArgNamespace():
	argNamespace = {}
	argName = ''
	for i in range(1, len(sys.argv)):
		if (sys.argv[i][0] == '-' or sys.argv[i][0:1] == '--'):
			if argName != '':
				argNamespace[argName] = True
			else:
				argName = sys.argv[i].replace('-', '')
		else:
			if argName != '':
				argNamespace[argName] = sys.argv[i]
				argName = ''
			else:
				argName = sys.argv[i]
	if argName != '':
		argNamespace[argName] = True
	return argNamespace

if __name__ == '__main__':
	# read args
	argNamespace = getArgNamespace()
	# debug print args
	print('Received args:')
	for key, value in argNamespace.items():
		print('\n\t' + str(key) + '=' + str(value))

	# read options
	optfile = argNamespace.get('options', '')
	if optfile != '':
		options_file = optfile
	else:
		options_file = os.getcwd() + '/options.json'
	print('\nReading options file: ' + options_file)
	with open(options_file, 'r', encoding='utf-8') as f:
		actions = json.load(f)

	# execute actions
	mainClicker = pySimpleClicker(actions)
	mainClicker.executeActions()
	print(mainClicker.textLog)

