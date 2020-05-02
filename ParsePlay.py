#!/bin/python3
import sys
from typing import List
import xmltodict

def exampleParsing(inst):
	for s in inst['sig']:
		if s['@label'] == 'Actor':
			count = 0
			for a in s['atom']:
				count += 1
			print("There are " + str(count) + " actors")

		if s['@label'] == 'Prop':
			count = 0
			for a in s['atom']:
				count += 1
			print("There are " + str(count) + " props")

		if s['@label'] == 'Scene':
			count = 0
			for a in s['atom']:
				count += 1
			print("There are " + str(count) + " scenes")

	for f in inst['field']:
		if f['@label'] == 'pre':
			for d in f['tuple']:
				atoms = d['atom']
				# this is printing the pre field, in order of event -> scene
				print(str(atoms[0]['@label']) + " comes after " + str(atoms[1]['@label']))

		if f['@label'] == 'post':
			for d in f['tuple']:
				atoms = d['atom']
				# this is printing the post field, in order of event -> scene
				print(str(atoms[0]['@label']) + " comes before " + str(atoms[1]['@label']))

		if f['@label'] == "carryOnAsignments":
			for d in f['tuple']:
				atoms = d['atom']
				# this is printing the carry on assignments, in order of event -> actor -> prop
				print("During " + str(atoms[0]['@label']) + ", " + str(atoms[1]['@label']) + " will carry on " + str(atoms[2]['@label']))

		if f['@label'] == "carryOffAsignments":
			for d in f['tuple']:
				atoms = d['atom']
				# this is printing the carry off assignments, in order of event -> actor -> prop
				print("During " + str(atoms[0]['@label']) + ", " + str(atoms[1]['@label']) + " will carry off " + str(atoms[2]['@label']))

def exampleParsing1(inst):
	numActors = 0
	numProps = 0
	numScenes = 0
	sceneList = []
	# maps scene to event
	preMap = {}
	postMap = {}
	# maps event to actor,prop
	carryOn = {}
	carryOff = {}

	init = None
	term = None

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
		if f['@label'] == 'pre':
			for d in f['tuple']:
				atoms = d['atom']
				preMap[atoms[1]['@label']] = atoms[0]['@label']

		if f['@label'] == 'post':
			for d in f['tuple']:
				atoms = d['atom']
				postMap[atoms[1]['@label']] = atoms[0]['@label']

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

		
	for s in sceneList:
		print(s)
		if s in postMap:
			precedingEvent = postMap[s]
			for t in carryOn[precedingEvent]:
				print(t[0] + " will carry on " + t[1])
		if s in preMap:
			followingEvent = preMap[s]
			for t in carryOff[followingEvent]:
				print(t[0] + " will carry off " + t[1])


if __name__ == "__main__":
	import xmltodict
	fd = open(sys.argv[1])
	doc = xmltodict.parse(fd.read())
	inst = doc['alloy']['instance']
	exampleParsing1(inst)

	