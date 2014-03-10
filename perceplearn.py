#!/usr/bin/python
# -*- coding: <encoding name> -*-

import sys;

######################################################################

#We look at this class as the base class for all development of perceptron. This contains the label and
#weight per label

class WordMapping :
    
	def __init__(self,word,weightPerLabel):
		self.word = word;
		self.weightPerLabel = weightPerLabel;
    
	
	def getDetails(self):
		return self.word+" "+str(self.weightPerLabel);

############################################################################################################################################

# This function is used to give the unique number of words in a particular type of classifier. The words are identitifed as case insensitive (meeting == Meeting == MeeTinG)


def getUniqueWordList(fileName,labelTypes):
	count = {};
	file = open(fileName,'r');
	for line in file :
		
		words = line.rstrip('\n\r').split(' ');
		words = words[1:len(words)];
		for w in words:
           		 if w in count:
				continue;
            		 else:
				weightPerLabel={};
				for label in labelTypes:
					weightPerLabel[label]=0;
				count[w] = WordMapping(w,weightPerLabel);
	file.close();
    
	return count;

############################################################################################################################################

def getLabelTypes(fileName):
	file = open(fileName,'r');
	count = 0;
	labelTypes = {};
	labelTypesOthers = {};
	for line in file:
        	word = line.split(' ')[0];
		if word in labelTypes:
			continue;
		else:
		   labelTypes[word]=word;
	file.close();
	return labelTypes;

################################################################################

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
		for label in sorted(labelTypes.keys()):
			sumValues[label] += wordMapping.weightPerLabel[label];
    
	max = -1;
	retLabel = "";
	for label in sumValues:
		if sumValues[label]> max:
			max = sumValues[label];
			retLabel = label;
	return retLabel;

#######################################################################################################

def updateList(passList,line,newLabel,actualLabel,labelTypes):
	
	line =  line[1:len(line)];
	for word in line:
		#word = word.upper();
		#if word in labelTypes:
        #	continue;
		#else:
	  if word in passList:	
		wordMapping = passList[word];
		wordMapping.weightPerLabel[newLabel]-=1;
		wordMapping.weightPerLabel[actualLabel]+=1;
	  


#############################################################################################################
def writeFile(fileName,list,labelTypes):
    modelFile = open(fileName.strip(),'w');
    totalLabelString = "$LABEL##";
    for label in sorted(labelTypes.keys()):
        totalLabelString += labelTypes[label]+' ';
    totalLabelString +='\n';
    modelFile.write(totalLabelString);
    for word in list:
        wordMapping = list[word];
        writeString = wordMapping.word.rstrip('\n\r')+"~##~";
        
        for label in sorted(labelTypes.keys()):
            writeString += labelTypes[label] + ' '+str(wordMapping.weightPerLabel[label])+"|";
	 	
        modelFile.write(writeString+'\n');
    modelFile.close();
#####################################################################################################



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



###################################################################################################
#First we fetch the file. Then we fetch the label types of the files. We need this to create the dictionary
#sort of structure required to store the total number of words and their counts.
#First we find the total unique words in the perceptron(except the labels). Then we create 2 lists : one which is
# a temp list to store the current weight for the pass. 2) Store the total weight for all the passes
# We also define N to be any larger value for the passes.
# Once we perform the perceptron process , we average all the weights and dump all the contents in the file
# in form of <Word>~~<Label>:<Weight>~|~<Label>:<Weight>



# Here we fetch the training file name from which we have to get the #messages
fileName = sys.argv[1];
labelTypes = getLabelTypes(fileName);
######################################################################
#Here we fetch the list of unique words, given the labels

averageList = getUniqueWordList(fileName,labelTypes);
fileTemp = open('buffer.txt','w');
fileTemp.close();
writeFile('buffer.txt',averageList,labelTypes);

N=21;

# Now for N passes, we do the following. We first create a buffer which stores the list of all the words
# and their weights. Next we scan each line in training file. Based on the existing weights, we calculate
# the sum of all weights per label.Pick label as the one with max weight. If that is the correct weight,OK.
# Else subtract 1 from all words in this line. Add 1 to all the other labels.
# On finish of all lines, add the weights to the averageList
#On finish of all passes, store the list into the model file as required.
for x in range(1,N):
	print "Pass "+str(x) + " of "+str(N-1)+" of the classifier";
		
	passList = prepareDictionary('buffer.txt');
	
	trainingfile = open(fileName,'r');
	for line in trainingfile :
	    line = line.rstrip('\n\r');
	    actualLabel = line.split(' ')[0];
	    newLabel = calculateMaxNewLabel(passList,line.split(' '),labelTypes);
	    if newLabel is not actualLabel:
                updateList(passList,line.split(' '),newLabel,actualLabel,labelTypes);
    
	for word in passList:
		for label in sorted(averageList[word].weightPerLabel.keys()):
			averageList[word].weightPerLabel[label] +=passList[word].weightPerLabel[label];
			
	
for word in averageList:
	wordMapping = averageList[word];
	for label in wordMapping.weightPerLabel:
		wordMapping.weightPerLabel[label] /= float(N-1);

writeFile(sys.argv[2],averageList,labelTypes);
