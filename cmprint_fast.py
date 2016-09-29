#!python3
from os import system
import sys
import random
import time

import colorama

import copy

import rightangles

import asciiart

# table of sin(1) to sin(90)
sin20 = [0.017, 0.034, 0.052, 0.069, 0.087, 0.104, 0.121, 0.139, 0.156, 0.173, 0.190, 0.207, 0.224, 0.241, 0.258, 0.275, 0.292, 0.309, 0.325, 0.342, 0.358, 0.374, 0.390, 0.406, 0.422, 0.438, 0.453, 0.469, 0.484, 0.5, 0.515, 0.529, 0.544, 0.559, 0.573, 0.587, 0.601, 0.615, 0.629, 0.642, 0.656, 0.669, 0.682, 0.694, 0.707, 0.719, 0.731, 0.743, 0.754, 0.766, 0.777, 0.788, 0.798, 0.809, 0.819, 0.829, 0.838, 0.848, 0.857, 0.866, 0.874, 0.882, 0.891, 0.898, 0.906, 0.913, 0.920, 0.927, 0.933, 0.939, 0.945, 0.951, 0.956, 0.961, 0.965, 0.970, 0.974, 0.978, 0.981, 0.984, 0.987, 0.990, 0.992, 0.994, 0.996, 0.997, 0.998, 0.9994, 0.9998, 1]

# table of cos(1) to cos(90)
cos20 = [0.9998, 0.9994, 0.998, 0.997, 0.996, 0.994, 0.992, 0.990, 0.987, 0.984, 0.981, 0.978, 0.974, 0.970, 0.965, 0.961, 0.956, 0.951, 0.945, 0.939, 0.933, 0.927, 0.920, 0.913, 0.906, 0.898, 0.891, 0.882, 0.874, 0.866, 0.857, 0.848, 0.838, 0.829, 0.819, 0.809, 0.798, 0.788, 0.777, 0.766, 0.754, 0.743, 0.731, 0.719, 0.707, 0.694, 0.682, 0.669, 0.656, 0.642, 0.629, 0.615, 0.601, 0.587, 0.573, 0.559, 0.544, 0.529, 0.515, 0.5, 0.484, 0.469, 0.453, 0.438, 0.422, 0.406, 0.390, 0.374, 0.358, 0.342, 0.325, 0.309, 0.292, 0.275, 0.258, 0.241, 0.224, 0.207, 0.190, 0.173, 0.156, 0.139, 0.121, 0.104, 0.087, 0.069, 0.052, 0.034, 0.017, 0]

c = list("................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................\
................................................................................")

def printToScreen(screen_table):
	# turn the table into a string
	output = listToString(screen_table)
	
	# move cursor to top left
	print('\x1b[1;1H', end='')
	
	# put stuff on screen
	sys.stdout.write(output.replace('.', ' '))
	sys.stdout.flush()
	#print(i)
	
	# wait a little while
	time.sleep(0.01)
	#a = input()

def listToString(list):
	output = ""
	
	for row in list:
		for pixel in row:
			output += pixel
	return output

def rotate2DTable(table, angle):
	
	# c is a "blank" table to insert the rotated points in
	global c
	
	# THE PROBLEM WAS RELATED TO PASS-BY-OBJECT-REFERENCE AND USING [:] ON A LIST OF LISTS
	output_table = copy.deepcopy(c)
	
	intermediate_table = []
	
	# if angle is more than any of the right angles,
	# start by fetching the precomputed table for that right angle,
	# then subtract the amount of that right angle from the angle variable
	if angle >= 90:
		if angle >= 180:
			if angle >= 270:
				intermediate_table = copy.deepcopy(rightangles.twohundredandseventy)
				angle = angle - 270
			else:
				intermediate_table = copy.deepcopy(rightangles.hundredandeighty)
				angle = angle - 180
		else:
			intermediate_table = copy.deepcopy(rightangles.ninety)
			angle = angle - 90
	# if angle is less than any of the right angles,
	# fetch the "zero" table
	else:
		intermediate_table = copy.deepcopy(rightangles.zero)

	# finally, if there's any more angle to rotate, rotate it and return
	if angle > 0:
		new_table = copy.deepcopy(intermediate_table)
		intermediate_table = ""
		intermediate_table = []
		
		# rotation
		for pixel in new_table:
			
			# move center to 0, 0
			x_shift = pixel[0] - 40
			y_shift = pixel[1] - 12
			
			# rotate pixel around 0, 0
			x1 = (x_shift * cos20[angle-1]) - (y_shift * sin20[angle-1])
			y1 = (y_shift * cos20[angle-1]) + (x_shift * sin20[angle-1])
			
			# move center back to where it should be
			x1 = x1 + 40
			y1 = y1 + 12
			
			intermediate_table.append((x1, y1, pixel[2], pixel[3]))
	
	# for each rotated pixel, if that pixel is still within the screen window,
	# add its "color" to its coordinate in the new 2D y, x array
	for pixel in intermediate_table:
		if 0 < pixel[0] < 80 and 0 < pixel[1] < 24:
			output_table[int(pixel[1])][int(pixel[0])] = table[pixel[3]][pixel[2]]
		
	return output_table

def main():
	
	global c

	b = []
	
	for y in range(24):
		row = 80 * y
		
		b.append(c[row:row + 80])
	
	new_c = []
	
	for y in range(24):
		row = 80 * y
		
		new_c.append(c[row:row + 80])
	
	c = new_c
	


	system('cls')

	colorama.init()
		
	new_b = []
	
	start_b = asciiart.start_b[0]

	for y in range(24):
		row = 80 * y
		new_b.append(start_b[row:row + 80])
	b = new_b[:]
	
	direction = True
	
	i = 0
	
	while True:
		
		printToScreen(new_b)
		#printToScreen(str(i))
		
		i = (i + 6) % 360
		
		new_b = rotate2DTable(b, i)

if __name__ == '__main__':
	main()