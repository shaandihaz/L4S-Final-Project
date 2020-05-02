#!/bin/python3
import sys
from typing import List
import xmltodict
import json 

numActors = 0
numProps = 0
numScenes = 0
sceneList = []
# maps scene to event
preMap = {}
postMap = {}
# maps event to scene
preMapRev = {}
postMapRev = {}
# maps event to actor,prop
carryOn = {}
carryOff = {}
# these are scenes
init = None
term = None
# maps scene to actor,prop
actorMap = {}
propMap = {}
# maps scene to a map from psoition to list of actor/prop
actorPosMap = {}
propPosMap = {}

def parse(inst):
	global numActors
	global numProps
	global numScenes
	global sceneList
	# maps scene to event
	global preMap
	global postMap
	# maps event to scene
	global preMapRev
	global postMapRev
	# maps event to actor,prop
	global carryOn
	global carryOff 
	# these are scenes
	global init
	global term
	# maps scene to actor,prop
	global actorMap
	global propMap
	# maps scene to a map from psoition to list of actor/prop
	global actorPosMap
	global propPosMap

	for s in inst['sig']:

		if s['@label'] == 'Actor':
			for a in s['atom']:
				numActors += 1

		if s['@label'] == 'Prop':
			for a in s['atom']:
				numProps += 1

		if s['@label'] == 'Scene':
			for a in s['atom']:
				sceneList.append(a['@label'])
				numScenes += 1

	for f in inst['field']:
		if f['@label'] == 'init':
			init = f['tuple']['atom'][1]['@label']

		if f['@label'] == 'term':
			term = f['tuple']['atom'][1]['@label']

		if f['@label'] == 'pre':
			for d in f['tuple']:
				atoms = d['atom']
				preMap[atoms[1]['@label']] = atoms[0]['@label']
				preMapRev[atoms[0]['@label']] = atoms[1]['@label']

		if f['@label'] == 'post':
			for d in f['tuple']:
				atoms = d['atom']
				postMap[atoms[1]['@label']] = atoms[0]['@label']
				postMapRev[atoms[0]['@label']] = atoms[1]['@label']

		if f['@label'] == "carryOnAsignments":
			for d in f['tuple']:
				atoms = d['atom']
				if atoms[0]['@label'] in carryOn:
					carryOn[atoms[0]['@label']].append([atoms[1]['@label'], atoms[2]['@label']])
				else:
					carryOn[atoms[0]['@label']] = [[atoms[1]['@label'], atoms[2]['@label']]]

		if f['@label'] == "carryOffAsignments":
			for d in f['tuple']:
				atoms = d['atom']
				if atoms[0]['@label'] in carryOff:
					carryOff[atoms[0]['@label']].append([atoms[1]['@label'], atoms[2]['@label']])
				else:
					carryOff[atoms[0]['@label']] = [[atoms[1]['@label'], atoms[2]['@label']]]

		if f['@label'] == 'props':
			for d in f['tuple']:
				atoms = d['atom']
				if atoms[0]['@label'] in propMap:
					propMap[atoms[0]['@label']].append(atoms[1]['@label'])
				else:
					propMap[atoms[0]['@label']] = [atoms[1]['@label']]

		if f['@label'] == 'actors':
			for d in f['tuple']:
				atoms = d['atom']
				if atoms[0]['@label'] in actorMap:
					actorMap[atoms[0]['@label']].append(atoms[1]['@label'])
				else:
					actorMap[atoms[0]['@label']] = [atoms[1]['@label']]

		if f['@label'] == "actorPos":
			for d in f['tuple']:
				atoms = d['atom']
				if atoms[0]['@label'] not in actorPosMap:
					actorPosMap[atoms[0]['@label']] = {"Left0": [], "Right0": [], "Center0": []}
				actorPosMap[atoms[0]['@label']][atoms[2]['@label']].append(atoms[1]['@label'])

		if f['@label'] == "propPos":
			for d in f['tuple']:
				atoms = d['atom']
				if atoms[0]['@label'] not in propPosMap:
					propPosMap[atoms[0]['@label']] = {"Left0": [], "Right0": [], "Center0": []}
				propPosMap[atoms[0]['@label']][atoms[2]['@label']].append(atoms[1]['@label'])

def printParse():
	s = init
	sceneCount = 0
	while True:
		print("Scene " + str(sceneCount))
		if s in postMap:
			precedingEvent = postMap[s]
			if precedingEvent in carryOn:
				for t in carryOn[precedingEvent]:
					print(t[0] + " carried on " + t[1])
		if s in actorMap:
			print("Actors in scene:", end=" ")
			for actor in actorMap[s]:
				print(actor, end=" ")
			print("")
		if s in propMap:
			print("Props in scene:", end=" ")
			for prop in propMap[s]:
				print(prop, end=" ")
			print("")
		if s in actorPosMap:
			print("Actors stage left:", end=" ")
			for actor in actorPosMap[s]["Left0"]:
				print(actor, end=" ")
			print("")
			print("Actors stage right:", end=" ")
			for actor in actorPosMap[s]["Right0"]:
				print(actor, end=" ")
			print("")
		if s in propPosMap:
			print("Props stage left:", end=" ")
			for prop in propPosMap[s]["Left0"]:
				print(prop, end=" ")
			print("")
			print("Props stage right:", end=" ")
			for prop in propPosMap[s]["Right0"]:
				print(prop, end=" ")
			print("")
		if s in preMap:
			followingEvent = preMap[s]
			if followingEvent in carryOff:
				for t in carryOff[followingEvent]:
					print(t[0] + " will carry off " + t[1])
		if s == term:
			break
		nextEvent = preMap[s]
		s = postMapRev[nextEvent]
		sceneCount += 1
		print("")

def parseToJson():
	bigMap = {"numActors" : numActors, "numProps": numProps, "numScenes": numScenes, "sceneData": {}}
	s = init
	sceneCount = 0
	while True:
		miniMap = {"carryOn": {}, "carryOff": {}, 
		"props": [], "actors": [], 
		"leftActors": [], "rightActors": [],
		"leftProps": [], "rightProps": []}
		if s in postMap:
			precedingEvent = postMap[s]
			if precedingEvent in carryOn:
				for t in carryOn[precedingEvent]:
					miniMap["carryOn"][t[0]] = t[1]
		if s in actorMap:
			for actor in actorMap[s]:
				miniMap["actors"].append(actor)
		if s in propMap:
			for prop in propMap[s]:
				miniMap["props"].append(actor)
		if s in actorPosMap:
			for actor in actorPosMap[s]["Left0"]:
				miniMap["leftActors"].append(actor)
			for actor in actorPosMap[s]["Right0"]:
				miniMap["rightActors"].append(actor)
		if s in propPosMap:
			for prop in propPosMap[s]["Left0"]:
				miniMap["leftProps"].append(actor)
			for prop in propPosMap[s]["Right0"]:
				miniMap["rightProps"].append(actor)
		if s in preMap:
			followingEvent = preMap[s]
			if followingEvent in carryOff:
				for t in carryOff[followingEvent]:
					miniMap["carryOff"][t[0]] = t[1]
		bigMap["sceneData"]["Scene " + str(sceneCount)] = miniMap
		if s == term:
			break
		nextEvent = preMap[s]
		s = postMapRev[nextEvent]
		sceneCount += 1

	return json.dumps(bigMap)


if __name__ == "__main__":
	import xmltodict
	fd = open(sys.argv[1])
	doc = xmltodict.parse(fd.read())
	inst = doc['alloy']['instance']
	parse(inst)
	print(parseToJson())

	