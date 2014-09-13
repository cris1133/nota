#! /home/cristopher/Enthought/Canopy_64bit/User/bin/python

import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time
from sets import Set
import thread
import random
from pyfiglet import figlet_format
from itertools import chain, repeat, islice
import os.path

## Workings
## buf holds a list of "blocks"
## Each "block" holds a list of "lines"
## Each "line" holds a string
## When the up arrow is pressed when the cursor is at y0
#### The offset changes, same for "down"
class Cursor:
	def __init__(self, y, x):
		self.y = y
		self.x = x

def main(stdscr):
	myscreen = curses.initscr()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
	buf = []
	bufN = 0
	buf.append([["" for n in range(4095)]])
	offset = 0
	offsetX = 0
	cursor = Cursor(1,0)
	key = 0
	mode = 0
	prog_run = 1
	save_name = ""
	prev_x = 0
	prev_y = 0
	curses.mousemask(1)
	curses.raw()

	def saveFile(name):
		if os.path.isfile(name):
			f = open(name,'r+')
		else: 
			f = file(name,'w')
		for line in buf[0][0]:
			if len(line) > 1:
				if line.startswith('\n'):
					f.write('\n')
				elif not line.endswith('\n'):
					f.write(line + '\n')
		f.close

	def openFile(name):
		if os.path.isfile(name):
			f = open(name,'r+')
			l = f.readlines()
			if len(l) > 4025:
				n = len(l) - 4025
				buf.append([["" for n in range(n)]])
			for line in range(len(l)):
				if l[line].startswith('\n'):
					continue
				if l[line].endswith('\n'):
					l[line] = l[line][:-1]
				buf[0][0][line + 1] = l[line]
			f.close

	def basicGUI():
		## Explanation of controls
		if x > 47:
			if mode == 0:
				myscreen.addstr(y-1, 0, "Save File - C^s", curses.color_pair(4))
				myscreen.addstr(y-1, 16, "Open File - C^o", curses.color_pair(4))
				myscreen.addstr(y-1, 32, "Export(HTML) - C^e", curses.color_pair(4))
			if mode == 1:
				myscreen.addstr(y-1, 0, "Save File - C^s", curses.color_pair(4))
				myscreen.addstr(y-1, 16, save_name, curses.color_pair(4))
			if mode == 2:
				myscreen.addstr(y-1, 0, "Open File - C^s", curses.color_pair(4))
				myscreen.addstr(y-1, 16, save_name, curses.color_pair(4))			

		## Indicators
		if cursor.y < 1:
			myscreen.addstr(0, 0, " "*(x), curses.color_pair(5))
			curses.curs_set(0)
		else:
			myscreen.addstr(0, 0, " "*(x), curses.color_pair(1))
			curses.curs_set(1)

		## The actual text
		## Loop goes here
		for string in range(len(buf[0][0])):
			if string < (y-2):

				## H3
				if string > 2:
					if string < len(buf[0][0]) and buf[0][0][(string-1) + offset].startswith("\t") and buf[0][0][(string) + offset].startswith("\t"*2) and buf[0][0][(string+1) + offset].startswith("\t"*3):
						myscreen.addstr(string, 0, buf[0][0][string + offset][(0+offsetX):((x-1) + offsetX)], curses.A_BOLD)
						continue

				## H2
				if string > 1:
					if string < len(buf[0][0]) and buf[0][0][(string) + offset].startswith("\t") and buf[0][0][(string+1) + offset].startswith("\t"*2) and not(buf[0][0][(string) + offset].startswith("\t"*2)) :
						myscreen.addstr(string, 0, buf[0][0][string + offset][(0+offsetX):((x-1) + offsetX)], curses.A_BOLD)
						continue
				## H1
				if string < len(buf[0][0]) and buf[0][0][(string + 1) + offset].startswith("\t") and not(buf[0][0][(string) + offset].startswith("\t")):
					myscreen.addstr(string, 0, buf[0][0][string + offset][(0+offsetX):((x-1) + offsetX)], curses.A_BOLD)
				else:
					myscreen.addstr(string, 0, buf[0][0][string + offset][(0+offsetX):((x-1) + offsetX)])

	while 1==prog_run:
		myscreen.clear()
		y, x = myscreen.getmaxyx()
		##########################

		if mode == 1 and key > 32 and key < 176:
			if key == 127:
				save_name = save_name[:-1]
				if cursor.x > 16:
					cursor.x = cursor.x - 1
			else:
				save_name = save_name + chr(key)
		elif key == curses.KEY_RESIZE:
			y, x = myscreen.getmaxyx()
		elif mode == 2 and key > 32 and key < 176:
			if key == 127:
				save_name = save_name[:-1]
				if cursor.x > 16:
					cursor.x = cursor.x - 1
			else:
				save_name = save_name + chr(key)
		elif key == curses.KEY_UP and mode == 0:
			if cursor.y > 0:
				cursor.y = cursor.y - 1
			if cursor.y < 1:
				curses.curs_set(0)
				if offset > 0:
					offset = offset-1
			cursor.x = min(len(buf[0][0][cursor.y + offset].replace('\t', "        ")), x-1)
		elif key == curses.KEY_DOWN and mode == 0:
			if cursor.y == y-3:
				offset = offset + 1
			else:
				cursor.y = cursor.y + 1
			if cursor.y > 0:
				curses.curs_set(1)
			cursor.x = min(len(buf[0][0][cursor.y + offset].replace('\t', "        ")), x-1)
		elif key == curses.KEY_RIGHT and mode == 0:
			if cursor.x < (x-1):
				cursor.x = cursor.x + 1
			else:
				offsetX = offsetX + 1
		elif key == curses.KEY_LEFT and mode == 0:
			if cursor.x > 0:
				cursor.x = cursor.x - 1
			else:
				if offsetX > 0:
					offsetX = offsetX - 1
		elif key == 19:
			if mode == 0:
				mode = 1
				prev_x = cursor.x
				prev_y = cursor.y
				cursor.x = 16
				cursor.y = y - 1
			else:
				mode = 0
				save_name = ""
				cursor.x = prev_x
				cursor.y = prev_y
		elif key == 15:
			if mode == 0:
				mode = 2
				prev_x = cursor.x
				prev_y = cursor.y
				cursor.x = 16
				cursor.y = y - 1
			else:
				mode = 0
				save_name = ""
				cursor.x = prev_x
				cursor.y = prev_y
		elif key == 27:
			prog_run = 0
		elif key == 127:
			isTab = 0
			tabOffset = 0
			if buf[0][0][cursor.y + offset].endswith('\t'):
				isTab = 1
			for character in buf[0][0][cursor.y + offset]:
				if character == '\t':
					tabOffset = tabOffset + 7
			buf[0][0][cursor.y + offset] = buf[0][0][cursor.y + offset][:(cursor.x+offsetX-1 - tabOffset)] + buf[0][0][cursor.y + offset][(cursor.x+offsetX- tabOffset):]
			if cursor.x > 0:
				cursor.x = cursor.x -1
				if isTab == 1:
					cursor.x = cursor.x - 7
			elif cursor.y > 0 and cursor.x == 0:
				if buf[0][0][cursor.y + offset] == "":
					del buf[0][0][cursor.y + offset]
				cursor.y = cursor.y - 1
				cursor.x = min(len(buf[0][0][cursor.y + offset].replace('\t', "        ")), x-1)
			if cursor.y == 0 and offset > 0:
				offset = offset-1
		elif key == 10:
			if mode == 0:
				if cursor.y == (y-3):
					offset = offset + 1
				elif cursor.x < len(buf[0][0][cursor.y + offset].replace('\t', "        ")) - 1:
					buf[0][0].insert((cursor.y + offset), "")
					cursor.y = cursor.y + 1
				else:
					cursor.y = cursor.y + 1
					if buf[0][0][cursor.y-1] == "":
						buf[0][0].insert((cursor.y + offset), "")
					cursor.x = min(len(buf[0][0][cursor.y + offset].replace('\t', "        ")), x-1)
			if mode == 1:
				mode = 0
				saveFile(save_name)
				save_name = ""
				cursor.x = prev_x
				cursor.y = prev_y
			if mode == 2:
				mode = 0
				openFile(save_name)
				save_name = ""
				cursor.x = prev_x
				cursor.y = prev_y
		elif key == curses.KEY_MOUSE:
			_, mx, my, _, _ = curses.getmouse()
			if my == y-1:
				if mx > 16 and mx < 32:
					if mode == 0:
						mode = 2
						prev_x = cursor.x
						prev_y = cursor.y
						cursor.x = 16
						cursor.y = y - 1
					else:
						mode = 0
						save_name = ""
						cursor.x = prev_x
						cursor.y = prev_y
				elif mx < 16:
					if mode == 0:
						mode = 1
						prev_x = cursor.x
						prev_y = cursor.y
						cursor.x = 16
						cursor.y = y - 1
					else:
						mode = 0
						save_name = ""
						cursor.x = prev_x
						cursor.y = prev_y				
			else:
				cursor.x = min(len(buf[0][0][cursor.y + offset].replace('\t', "        ")), x-1)
				cursor.y = my
		elif key != 0  and mode == 0:
			tabOffset = 0
			for character in buf[0][0][cursor.y + offset]:
				if character == '\t':
					tabOffset = tabOffset + 7
			if len(buf[0][0][cursor.y + offset]) < (cursor.x + offsetX - tabOffset):
				buf[0][0][cursor.y + offset] = buf[0][0][cursor.y + offset] + chr(key)
			else:
				buf[0][0][cursor.y + offset] = buf[0][0][cursor.y + offset][:cursor.x + offsetX - tabOffset] + chr(key) + buf[0][0][cursor.y + offset][cursor.x + offsetX - tabOffset:]
			if key == 9 and cursor.x < (x-8):
				cursor.x = cursor.x + 7
			if cursor.x < (x-2):
				cursor.x = cursor.x + 1
			else: 
				cursor.y = cursor.y + 1
				cursor.x = min(len(buf[0][0][cursor.y + offset].replace('\t', "        ")), x-1)
		
		## Basic GUI
		basicGUI()
		
		## Move cursor to the proper position
		if cursor.y > 0:
			myscreen.move(cursor.y, cursor.x)
		else:
			myscreen.move(1, cursor.x)

		#####################
		myscreen.refresh()
		key = myscreen.getch()

wrapper(main)
