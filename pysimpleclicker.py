import cv2
import time
import numpy as np
import pyscreenshot as ImageGrab
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
		patt = cv2.imread(imgPath, 0)
		for i in range(0, repeatCount):
			screenshot = ImageGrab.grab()
			img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
			h, w, points = self.__findImageByPattern(img, patt, 0.80)
			if len(points[0]) != 0:
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
			self.errorFlag = False
		return h, w, points

	def __executeActionTypeClickToImgLeft(self, imgPath, repeatCount, repeatDelay, endDelay):
		textLog = '\n\tLeft click by Image (by pattern: ' + imgPath + ')'
		h, w, points = self.__executeActionTypeWaitFoImg(imgPath, repeatCount, repeatDelay, endDelay)
		if self.errorFlag == False:
			pyautogui.moveTo(points[0][0] + w / 2, points[1][0] + h / 2)
			for i in range(0, repeatCount):
				pyautogui.click()
				self.textLog += textLog
				if i < repeatCount and repeatDelay > 0:
					time.sleep(repeatDelay)
			if endDelay > 0:
				time.sleep(endDelay)

	def __executeActionTypePushKeyboard(self, keyValue, repeatCount, repeatDelay, endDelay):
		for i in range(0, repeatCount):
			pyautogui.keyDown(keyValue)
			pyautogui.keyUp(keyValue)
			self.textLog += '\n\tPush key "' + keyValue + '"'
			if i < repeatCount and repeatDelay > 0:
				time.sleep(repeatDelay)
		if endDelay > 0:
			time.sleep(endDelay)

	def executeActions(self):
		for action in actions:
			curTextError = ''
			# prepare action values
			actionType = action.get('type', '')
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
				if actionType == 'ClickToImg':
					self.__executeActionTypeClickToImgLeft(actionValue, actionCount, actionDelay, actionSleep)
				elif actionType == 'PushKeyboard':
					self.__executeActionTypePushKeyboard(actionValue, actionCount, actionDelay, actionSleep)
				elif actionType == 'WaitForImage':
					self.__executeActionTypeWaitFoImg(actionValue, actionCount, actionDelay, actionSleep)

	def __findImageByPattern(self, image, imagePattern, overlapPart):
		img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		(patt_H, patt_W) = imagePattern.shape[:2]
		res = cv2.matchTemplate(img_grey, imagePattern, cv2.TM_CCOEFF_NORMED)
		loc = np.where(res > overlapPart)
		return patt_H, patt_W, loc[::-1]

def getArgNamespace():
	argNamespace = {}
	argName = ''
	for i in range(1, len(sys.argv)):
		if (sys.argv[i][0] == '-' or sys.argv[i][0:1] == '--'):
			if argName != '':
				argNamespace[argName] = True
			else:
				argName = sys.argv[i].replace('-', '')
				if argName == 'o':
					argName = 'options'
		else:
			if argName != '':
				argNamespace[argName] = sys.argv[i]
			else:
				argNamespace['options'] = sys.argv[i]
			argName = ''
	if argName != '':
		argNamespace[argName] = True
	return argNamespace

if __name__ == '__main__':
	# read args
	argNamespace = getArgNamespace()
	optfile = argNamespace.get('options', '')
	if optfile != '':
		options_file = optfile
	else:
		options_file = os.getcwd() + '/options.json'
	with open(options_file, 'r', encoding='utf-8') as f:
		actions = json.load(f)
	# debug print args
	for key, value in argNamespace.items():
		print(str(key) + '=' + str(value))
	sys.exit()

	mainClicker = pySimpleClicker(actions)
	mainClicker.executeActions()
	print(mainClicker.textLog)

