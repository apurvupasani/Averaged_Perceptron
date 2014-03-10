
#!/usr/bin/python
# -*- coding: <encoding name> -*-

import sys;
######################################################################

# Class used to store the word and its mapping

#We look at this class as the base class for all development of perceptron. This contains the label and 
#weight per label

class WordMapping :

	def __init__(self,word,weightPerLabel):
		self.word = word;
		self.weightPerLabel = weightPerLabel;
		
	
	def getDetails():
		return self;

class FScoreMatcher:
	def __init__(self,actualValue,classifiedValue):
		self.actualValue = actualValue;
		self.classifiedValue =classifiedValue;
	def getDetails():
		return self;
######################################################################

def prepareDictionary(fileName):
	dictionary = {};
	modelFile = open(fileName,'r');
	
	for line in modelFile:
		line  = line.rstrip('\n\r');
		if len(line) > 0 :
			if line.startswith('$') :
				continue;
			else:
				word = line.split('~##~')[0];
				classifiers = line.split('~##~')[1].split("|");
		
				countsPerLabel={};

				for text in classifiers:
					classifierText = text.strip().split(' ');
					if len(classifierText) != 1: 
						countsPerLabel[classifierText[0]] = float(classifierText[1]);

				wordMapping = WordMapping(word,countsPerLabel);
				dictionary[word] = wordMapping;
	modelFile.close();
	return dictionary;
#####################################################################################

#########################################################################################################3
def prepareMetaDataInfo(fileName):
	metaData = {};
	modelFile = open(fileName,'r');
	
	for line in modelFile:
		line = line.rstrip('\n\r');
		if len(line)>0 and line.startswith('$'):

			if line.startswith('$LABEL##') :
				labels = line.strip().split("##")[1].split(' ');
						
	return labels;	
##################################################################################################

def calculateMaxNewLabel(passList,line,labelTypes):
    	sumValues={};
	for label in labelTypes:
		sumValues[label]=0;
	line =  line[1:len(line)];
    
	for word in line:
		#word = word.upper();
		#if word in labelTypes:
        #	continue;
		#else:
	    if word in passList:	
		wordMapping = passList[word];
		for label in labelTypes:
			sumValues[label] += wordMapping.weightPerLabel[label];
    
	max = -1;
	retLabel = "";
	for label in sumValues:
		if sumValues[label]> max:
			max = sumValues[label];
			retLabel = label;
	return retLabel;


#####################################################################################################
modelFile = sys.argv[1].strip();	
labelTypes = prepareMetaDataInfo(modelFile);
dictionary = prepareDictionary(modelFile);
testFile = sys.stdin;
for line in testFile:
	actualLabel = line.split(' ')[0];
	newLabel = calculateMaxNewLabel(dictionary,line.split(' '),labelTypes);
	print newLabel;
	




