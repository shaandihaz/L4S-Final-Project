#!/bin/python3
import sys
from typing import List

tab = "    "

if __name__ == "__main__":
	name = input("Name your play! ")
	output = "inst " + name + " { \n"  + tab

# overall scenes
	numScene = input("How many scenes? ")
	numScene = int(numScene)
	output += "Scene = Scene0"
	for x in range(numScene):
		output += " + Scene" + str(x + 1)
	output += " + Scene" + str(numScene + 1) + "\n" + tab

# specify events
	output += "Event = Event0"
	for x in range(numScene):
		output += " + Event" + str(x + 1)
	output += "\n" + tab

# overall actors
	numActor = input("How many actors? ")
	numActor = int(numActor)
	output += "Actor = Actor0"
	for x in range(numActor - 1):
		output += " + Actor" + str(x + 1)
	output += "\n"  + tab

# overall props
	numProp = input("How many props? ")
	numProp = int(numProp)
	output += "Prop = Prop0"
	for x in range(numProp - 1):
		output += " + Prop" + str(x + 1)
	output += "\n"  + tab

# get scene info
	actorMap = {}
	propMap = {}
	for x in range(numScene):
		actorsInput = input("Which actors are in scene " + str(x)  + 
			"? Enter them 0-indexed and separated by spaces. ")
		sceneActors = actorsInput.split()
		actorMap[x] = sceneActors

		propsInput = input("Which props are in scene " + str(x)  + 
			"? Enter them 0-indexed and separated by spaces. ")
		sceneProps = propsInput.split()
		propMap[x] = sceneProps

# scene actors
	output += "actors = "
	for x in range(numScene):
		for a in actorMap[x]:
			output += "Scene" + str(x) + "->" + "Actor" + a + " + "

	output = output[:-3]
	output += "\n"  + tab

# scene props
	output += "props = "
	for x in range(numScene):
		for a in propMap[x]:
			output += "Scene" + str(x) + "->" + "Prop" + a + " + "
	
	output = output[:-3]
	output += "\n}"
	print(output)


