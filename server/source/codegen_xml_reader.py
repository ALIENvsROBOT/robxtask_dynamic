#!/usr/bin/env python
# coding=utf-8
import xml.etree.ElementTree as ET

indent = 0
counter_skip1 = 3
#--------------------------------------------
# Helper class to hold infos of one block
#--------------------------------------------
class SimpleBlockEntry():	

	def __init__(self, assetName, blockName, blockSlotName, blockSlotValue,indent):
		self.assetName = assetName
		self.blockName = blockName
		self.blockSlotName = blockSlotName
		self.blockSlotValue = blockSlotValue
		self.indent = indent

#--------------------------------------------
# Class to parse XML File from Blockly
#--------------------------------------------
# Author: SRFG, Mathias Schmoigl-Tonis
# Project: ROBxTASK
# Date: Q1-Q2 2022
#--------------------------------------------
class XML_BlocklyProject_Parser():

	#--------------------------------------------
	# CTOR: init class with variable members
	#--------------------------------------------
	def __init__(self, xmlString):
		self.root = []
		#self.tree = ET.parse(fileName)

		#self.root = self.tree.getroot()
		read_xml = ET.fromstring(xmlString)

		for i in range(len(read_xml)):
			if read_xml[i].tag == "{https://developers.google.com/blockly/xml}block":
				self.root.append(read_xml[i])

		self.listBlocks = []

	#--------------------------------------------
	# read the assets involved in the script
	#--------------------------------------------
	def readAssets(self):

		print ("Searching for all involved assets...")
		# for asset in self.root:
		# 	print ("-----------------------------------------------------")
		# 	print ("Found involved Asset with following tag and attrib: ")		
		# 	print ("^^^^^^^^^^",asset.tag, asset.attrib)
		# 	print ("-----------------------------------------------------")

		for i in range(len(self.root)):
			blocks = self.readBlocks(self.root[i])
			self.listBlocks.append(blocks)

	#--------------------------------------------
	# read all blocks at once
	#--------------------------------------------
	def readBlocks(self, asset):
		global counter_skip1

		print ("Parsing XML Tree searching for blocks...")
		print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		parent_end = 0

		for i in asset.iter('{https://developers.google.com/blockly/xml}block'):
			
			if i.attrib.get('type') == "controls_if" or i.attrib.get("type")=="controls_repeat_ext":
				print("parent",i.attrib,i.text," The indent is ",parent_end)
				parent_end += 1
				print("########################################")
				if i.tag == "{https://developers.google.com/blockly/xml}statement":
					print("==============")
				# for k in i.iter()
				# for j in i.iter():
				# 	print("child",j.attrib, j.text)
				# 	if j.attrib == {}:
				# 		print("found end point")
				# print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
 
		# variables needed for appending blocks to block list
		blockCounter = 0
		blocks = []
		blocks.append(SimpleBlockEntry("", [],[],[],None))

		# statementBlockCounters contains all statement counters, which are needed to 
		# count down the number of blocks within Statement (Loop or Selection)
		statementBlockCounters = [] 


		## there is a bug so it skips the first line so I include this logic
		# print("^^^^^^^^^^^^^^^^",asset.attrib,asset.text)

	
		for entry in asset.iter():
			# if counter_skip1 >= 1:
			# 	counter_skip1 -= 1
			# 	continue
			# print("111111",entry.tag)
				
			if(entry.tag=="{https://developers.google.com/blockly/xml}next"):
				print ("Found <next>-attribute")

				# Add a Stament End Tag, when any counter is zero again (reached end of a statement)
				
				for index in range(len(statementBlockCounters)):
				    
					if(statementBlockCounters[index] > 0):
						statementBlockCounters[index] -= 1
						if (statementBlockCounters[index] == 0):
							blockCounter += 1
							blocks.append(SimpleBlockEntry("", ["STATEMENT_ENDTAG"],["STATEMENT_ENDTAG"],["STATEMENT_ENDTAG"],"end"))
							
				
				# remove all zeros from array
				statementBlockCounters = [i for i in statementBlockCounters if i > 0]

				# normally start a new block
				blockCounter += 1

				blocks.append(SimpleBlockEntry("", [],[],[],None))
			
			if(entry.tag=="{https://developers.google.com/blockly/xml}statement"):
				if entry.attrib.get('name') == "ELSE":
					blocks.append(SimpleBlockEntry("", ["STATEMENT_ENDTAG"],["STATEMENT_ENDTAG"],["STATEMENT_ENDTAG"],"end"))
					blocks[blockCounter].blockName.append("ELSE       ")
					print("88888888888888888888888888888", "    detent")
					print ("Found <block>-attribute with type = " + entry.attrib.get('name'))
				hello = entry.findall("{https://developers.google.com/blockly/xml}statement")
				print("888888888888888888888888888888888",hello)

				
				# print ("---parent---",entry.attrib,entry.text)
				# for j in entry.iter("{https://developers.google.com/blockly/xml}statement"):
				# 	print("---first child---",j.attrib, j.text, j.tag)

				# 	if j.tag == "{https://developers.google.com/blockly/xml}statement":
				# 		for k in j.iter("{https://developers.google.com/blockly/xml}statement"):
				# 			for l in k.iter():
				# 				print("--- Second child ---",l.tag, l.attrib, l.text)
				# 		print("------- END --------")

					# if j.attrib.get('type') == "controls_if" or j.attrib.get("type")=="controls_repeat_ext":
					# 	print("======= LOL we are here")
					# else:
					# 	print("========",j.attrib, j.text,)


				# normally start a new block
				blockCounter += 1
				blocks.append(SimpleBlockEntry("", [],[],[],None))

				# we are starting a statement and need to find the end of Selection or Loop
				# count (nr of "next"-children + 1) to get actual nr of subnodes of statement block
				statementBlockCounters.append(len(list(entry.iter('{https://developers.google.com/blockly/xml}next'))) + 1)

			elif(entry.tag=="{https://developers.google.com/blockly/xml}block"):
				# Try using block and 2nd iter as statement tag you can find something from that
				# if entry.attrib.get("type")== "controls_if" or entry.attrib.get("type")=="controls_repeat_ext":
				# 	print("parent",entry.attrib,entry.text," The indent is ",parent_end)
				# 	parent_end += 1
				# 	print("########################################")
				# 	for j in entry.iter():
				# 		print("child",j.attrib, j.text)
				# 		if j.attrib == {}:
				# 			print("oooooooooooooooooooooooooooooooooo")
				# 	print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
				# else:
				print ("Found <block>-attribute with type = " + entry.attrib.get('type') + " and 'id = " + entry.attrib.get('id'),entry.text)
				blocks[blockCounter].blockName.append(entry.attrib.get('type'))
					
			elif(entry.tag=="{https://developers.google.com/blockly/xml}value"): 
				print ("Found <value>-attribute with name = " + entry.attrib.get('name'),entry.text)
				blocks[blockCounter].blockSlotName.append(entry.attrib.get('name'))
				
			elif(entry.tag=="{https://developers.google.com/blockly/xml}field"):
				print ("Found <field>-attribute with name = " + entry.attrib.get('name'),entry.text)
				blocks[blockCounter].blockSlotValue.append(entry.text)	
			


				
			else:
				print ("detent--------------",entry.tag)

		

		self.assignBlocksToAssets(blocks) # now put everything in order assigned to correct asset
		return blocks
			
	#--------------------------------------------
	# assign all blocks to an asset
	#--------------------------------------------
	def assignBlocksToAssets(self, blocks):
		
		# assign blocks
		assetName = ""
		for entry in blocks:
			if entry.blockName != []:
				block_string = entry.blockName[0]
				split_block_string = block_string.split("_")
				
				if "30:9c:23:84:fe:51" in split_block_string:
					assetName = "panda"
					entry.assetName = assetName

				elif "00:e0:4c:68:02:30" in split_block_string:
					assetName = "chasi"
					entry.assetName = assetName

				elif "b8:27:eb:24:1f:b2" in split_block_string:
					assetName = "qbo"
					entry.assetName = assetName

				print('\nFound entry: ' + entry.assetName + '; ' + entry.blockName[0] + '; ' + entry.blockSlotValue[0])
			
		# 	if(entry.blockName[0] == "SetAsset"):
		# 		assetName = entry.blockSlotValue[0]
			
			
				
		# # remove asset blocks
		# for entry in blocks:

		# 	if(entry.blockName[0] == "SetAsset"):
		# 		blocks.remove(entry)

	#--------------------------------------------
	# GETTER: return listBlock member variable
	#--------------------------------------------
	def getList(self):
		return self.listBlocks