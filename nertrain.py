#!/usr/bin/python
# -*- coding: <encoding name> -*-

import os;
import sys;
# Open the training file and append NULLELEM/NULLELEM at the beginning and at the end. This is done
# to ensure that the we dont have to worry about the data and convert to the features. Once we do that,
# we go on reading the each line and start converting it into the feature. We see that the previous tag 
# and the next value is stored, unless the tag is null in which case the details are skipped. 
# It will be something like this:

# Input : NULLELEM/NULLELEM This/DT is/VBZ a/DT test/NN NULLELEM/NULLELEM

# Output : DT NULLELEM This is
#	   VBZ DT	is  a   

# In short CurrentTag PrevTag CurrentWord Next Word and store them in a feature training file. 
# The output will be given to perceptron which will generate model file
class WordTagger :

	def __init__(self,word,tag):
		self.word = word;
		self.tag = tag;
		
	
	def getDetails():
		return self;


def fetchProperWords(word):
	arr = word.split("/");
	bag = {};
	if len(arr) == 3:
		bag[0] = arr[0]+"/"+arr[1];
		bag[1] = arr[2];
		return bag;	
	else:
		word = arr[0];
		for i in range(1,len(arr)-2):
			word+="/"+arr[i];
		word+="/"+arr[len(arr)-2];
		bag[0] = word;
		bag[1] = arr[len(arr)-1];
		return bag;


	
def preprocessData(file,writeFile):
	
	for line in file:
	   beforeLine = "BOS/BOS/BOS BOS/BOS/BOS ";
           afterLine = "EOS/EOS/EOS"; 
       	   line = line.strip("\n\r");
	   line = beforeLine+line+afterLine;
	   arrWords = line.split(' '); 		
           for i in range(2,len(arrWords)-2):
		prevPrevWord = fetchProperWords(arrWords[i-2])[0];
                prevWord = fetchProperWords(arrWords[i-1])[0];    	
		word = fetchProperWords(arrWords[i])[0];        
		tag = fetchProperWords(arrWords[i])[1];	
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
                writeFile.write(tag+" w:"+word+" p1:"+prevWord+" p2:"+prevPrevWord+" e1:"+nextWord+" s1:"+suffWord+"\n");#+" s2:"+suffPrevWord



writeFile = open(sys.argv[2],'w');	
trainFile = open(sys.argv[1],'r');
preprocessData(trainFile,writeFile); 

