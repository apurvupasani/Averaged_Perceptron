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

	         	 
def fetchProperWords(word):
	arr = word.split("/");
	bag = {};
	if len(arr) == 2:
		bag[0] = arr[0]+"/"+arr[1];
		#bag[1] = arr[2];
		return bag;	
	else:
		word = arr[0];
		for i in range(1,len(arr)-1):
			word+="/"+arr[i];
		#word+="/"+arr[len(arr)-1];
		bag[0] = word;
		#bag[1] = arr[len(arr)-1];
		return bag;


def processData(file,labelTypes,dictionary):
	labels  = {};
	labelCounter = 0;	
	
	for line in file:
	  output = '';
	  beforeLine = "BOS/BOS/BOS BOS/BOS/BOS ";
          afterLine = "EOS/EOS/EOS"; 
       	  line = line.strip("\n\r");
	  line = beforeLine+line+afterLine;
	  arrWords = line.split(' '); 	
          for i in range(2,len(arrWords)-2):
		prevPrevWord = fetchProperWords(arrWords[i-2])[0];
                prevWord = fetchProperWords(arrWords[i-1])[0];    	
		word = fetchProperWords(arrWords[i])[0];        
		#tag = fetchProperWords(arrWords[i])[1];	
		nextWord = fetchProperWords(arrWords[i+1])[0];
		suffWord = word.split("/")[0];
		if len(suffWord) > 2:
			suffWord = suffWord[len(suffWord)-2:len(suffWord)];
                else:
  			suffWord = suffWord;
	
		suffPrevWord = prevWord.split("/")[0];

		if len(suffPrevWord) > 2:
                    suffPrevWord = suffPrevWord[len(suffPrevWord)-2:len(suffPrevWord)];
                else :
                     suffPrevWord = suffPrevWord;	 

                newLine = "w:"+word+" p1:"+prevWord+" p2:"+prevPrevWord+" e1:"+nextWord+" s1:"+suffWord+" s2:"+suffPrevWord+"\n";
		newLabel = calculateMaxNewLabel(dictionary,newLine,labelTypes);
		output+= word+'/'+newLabel+' ';
	  print output+'\n';			
        return labels;

##################################################################################################
modelFile = sys.argv[1].strip();	
labelTypes = prepareMetaDataInfo(modelFile);
dictionary = prepareDictionary(modelFile)
labels = processData(sys.stdin,labelTypes,dictionary); 

