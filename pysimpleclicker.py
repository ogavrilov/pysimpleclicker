import cv2
import time
import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
import os
import json
import sys

def find_patt(image, patt, thres):
	img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	(patt_H, patt_W) = patt.shape[:2]
	res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res>thres)
	return patt_H, patt_W, loc[::-1]


if __name__ == '__main__':
	if len(sys.argv) > 1:
		options_file = sys.argv[1]
	else:
		options_file = os.getcwd() + '/options.json'
	with open(options_file, 'r', encoding='utf-8') as f:
		actions = json.load(f)

	debug = True
	if len(sys.argv) > 2:
		debug = True
	
	MyErrorFlag = False
	try:
		if debug:
			print('read parameters (' + str(len(actions)) + ') from file: ' + options_file)
	except Exception as errorObject:
		print('read parameters from file (' + options_file + '), error: ' + str(errorObject))
		MyErrorFlag = True

	if MyErrorFlag == False:
		for action in actions:
			ActionType = action.get('type', '')
			ActionValue = action.get('value', '')
			ActionCount = int(action.get('count', 0))
			ActionSleep = int(action.get('sleep', 0)) / 1000
			ActionDelay = int(action.get('delay', 0)) / 1000
			if debug:
				print('Action |type:' + ActionType + '|value:' + ActionValue + '|count:' + str(ActionCount) + '|sleep:' + str(ActionSleep) + '|delay:' + str(ActionDelay) + '|')
			if ActionType == '':
				print('action error: Type incorrect')
			elif ActionType == 'ClickToImg':
				if ActionValue == '':
					print('action error: Value incorrect')
				else:
					screenshot = ImageGrab.grab()
					img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1],screenshot.size[0],3)) 
					patt = cv2.imread(ActionValue, 0)
					h,w,points = find_patt(img, patt, 0.80)
					if len(points[0])!=0:
						pyautogui.moveTo(points[0][0]+w/2, points[1][0]+h/2)
						for i in range(0, ActionCount):
							pyautogui.click()
						if ActionSleep > 0:
							time.sleep(ActionSleep)
						if debug:
							print('done')
					else:
						print('action error: image area not found')
			elif ActionType == 'PushKeyboard':
				for i in range(0, ActionCount):
					pyautogui.keyDown(ActionValue)
					if ActionDelay > 0:
						time.sleep(ActionDelay)
					pyautogui.keyUp(ActionValue)
				if ActionSleep > 0:
					time.sleep(ActionSleep)
				if debug:
					print('done')
			elif ActionType == 'WaitForImage':
				patt = cv2.imread(ActionValue, 0)
				for i in range(0, ActionCount):
					screenshot = ImageGrab.grab()
					img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1],screenshot.size[0],3))
					h,w,points = find_patt(img, patt, 0.80)
					if len(points[0])!=0:
						if debug:
							print('done')
						break
					else:
						if debug:
							print('wait')
				if ActionDelay > 0:
					time.sleep(ActionDelay)