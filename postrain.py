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



def preprocessData(file,writeFile):
	
	for line in file:
	   beforeLine = "BOS/BOS BOS/BOS ";
           afterLine = " EOS/EOS"; 
       	   line = line.strip("\n\r");
	   line = beforeLine+line+afterLine;
	   arrWords = line.split(' '); 	
           for i in range(2,len(arrWords)-2):
		prevPrevWord = arrWords[i-2].split("/")[0];
                prevWord = arrWords[i-1].split("/")[0];	
		word = arrWords[i].split("/")[0];
		tag = arrWords[i].split("/")[1];
		nextWord = arrWords[i+1].split("/")[0];
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
		
                writeFile.write(tag+" w:"+word+" p1:"+prevWord+" e1:"+nextWord+" s1:"+suffWord+"\n"); #" pr1:"+prefPrevWord+" p2:"+prevPrevWord+" s2:"+ suffPrevWord +



writeFile = open(sys.argv[2],'w');	
trainFile = open(sys.argv[1],'r');
preprocessData(trainFile,writeFile); 


	

	 	

	
