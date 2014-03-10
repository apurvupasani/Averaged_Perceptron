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
			if line.startswith('$LABEL') :
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


def calculateMaxNewLabel(passList,line,labelTypes):
	sumValues={};
	for label in labelTypes:
		sumValues[label]=0;
	
	for word in line.split(' '):
		if word in passList:
			wordMapping = passList[word];
			for label in labelTypes:
				value = wordMapping.weightPerLabel[label];
				sumValues[label] += value;
			
	max = -1;
	retLabel = '';
	for label in sumValues:
		if sumValues[label]>max:
			max = sumValues[label];
			retLabel = label;
	return retLabel;

def processData(file,labelTypes,dictionary):
	labels  = {};
	labelCounter = 0;	
	
	for line in file:
           output = '';
           beforeLine = "BOS BOS ";
           afterLine = " EOS"; 
       	   line = line.strip("\n\r");
	   line = beforeLine+line+afterLine;
	   arrWords = line.split(' '); 	
           for i in range(2,len(arrWords)-2):
		prevPrevWord = arrWords[i-2];
                prevWord = arrWords[i-1];	
		word = arrWords[i];
		nextWord = arrWords[i+1];
		suffWord = word;
	        prefWord = word;	
		if len(suffWord) > 2:
			suffWord = word[len(word)-2:len(word)];
	 	        prefWord = word[0:2];	
       

		suffPrevWord = prevWord;
	        prefPrevWord = prevWord;	
		if len(suffPrevWord) > 2:
                    suffPrevWord = prevWord[len(prevWord)-2:len(prevWord)];
                    prefPrevWord = prevWord[0:2];
                newLine = "w:"+word+" p1:"+prevWord+" p2:"+prevPrevWord+" e1:"+nextWord+" s1:"+suffWord+" s2:"+suffPrevWord+"\n"; #" pr1:"+prefPrevWord+" +" s2:"+suffPrevWord
		newLabel = calculateMaxNewLabel(dictionary,newLine,labelTypes);
		output+= word+'/'+newLabel+' ';
	   print output+'\n';			
        return labels;

##################################################################################################
modelFile = sys.argv[1].strip();	
labelTypes = prepareMetaDataInfo(modelFile);
dictionary = prepareDictionary(modelFile)
labels = processData(sys.stdin,labelTypes,dictionary); 


