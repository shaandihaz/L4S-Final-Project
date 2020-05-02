#!/bin/python3
import sys
from typing import List
import xmltodict

def exampleParsing1(inst):
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

	s = init
	sceneCount = 0
	while True:
		print("Scene " + str(sceneCount))
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
		if s in postMap:
			precedingEvent = postMap[s]
			if precedingEvent in carryOn:
				for t in carryOn[precedingEvent]:
					print(t[0] + " will carry on " + t[1])
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



if __name__ == "__main__":
	import xmltodict
	fd = open(sys.argv[1])
	doc = xmltodict.parse(fd.read())
	inst = doc['alloy']['instance']
	exampleParsing1(inst)

	